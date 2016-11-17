__author__ = 'Michael'
import tree_manipulator as trman
import json, colorsys
import ConfigParser
from usersettingsclasses import PhylostratorUserSettings
import os

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if not cls.instance:
            # Not created or has been Destroyed
            obj = super(Singleton, cls).__call__(*args, **kw)
            cls.instance = obj
        return cls.instance


class Options(PhylostratorUserSettings):
    __metaclass__ = Singleton
    def __init__(self):
        PhylostratorUserSettings.__init__(self)
        self.def_settings_path = os.path.join('resources','default_settings.cfg')
        self.read_config_filepath(self.def_settings_path)


        #deprecated and should be deleted
        # self.cfg = ConfigParser.ConfigParser()
        # self.cfg.read('init_settings.cfg')

        # self.init_tree = self.cfg.get('main','initial_tree')
        # self.init_annotation = self.cfg.get('main', 'initial_annotation_file')
        # self.jitter_radius = self.cfg.getint('cairo','jitter_radius')
        # self.temp_subtree_path = self.cfg.get('main','temp_subtree_path')

class Controller():
    __metaclass__ = Singleton
    def __init__(self):
        self.apm=trman.AnnotatedPhylogramModel()
        self.current_uniques=[]
        self.annotation=None
        self.value_picker_ctrl=None
        self.bw_aspect_ratio=1.0

        #Drawing Properties:
        self.circle_size=None
        self.max_data_dims=None
        self.view_range=None

        #File Properties
        self.circle_sets_by_color = None
        # self.tree_file=None
        # self.annotation_file=None

    def save_model_to_file(self):
        #TODO: implement this
        self.apm.last_circle_size=self.circle_size
        self.apm.last_view_range=None
        # save the thing...
        pass

    def set_BufferedWindow_reference(self,bw_pointer):
        self.buffered_window=bw_pointer

    def set_cairo_draw_count_label(self,ct):
        self.image_frame.control_panel.m_stCairoDrawCount.SetLabel('Draw Count: %s' % ct)

    def set_tree_rotation(self,rotation):
        self.buffered_window.set_rotation(rotation)

    def get_relevent_data_from_model(self):
        print "getting relevant data from model"
        self.max_data_dims=self.buffered_window.radial_phylogram.get_max_dims()
        print "getting leaf coordinate data copy"
        self.leaf_coords=self.buffered_window.radial_phylogram.leaf_node_coords
        print "getting the node_annotation fields"
        # self.annotation_fields=self.annotation.annotation_fields
        self.annotation_fields = self.annotation.headers

    def set_ValuePickerCtrl_reference(self,vpc_pointer):
        self.value_picker_ctrl=vpc_pointer

    def set_ImageFrame_referenece(self,img_frame):
        self.image_frame=img_frame

    def set_zoompanel_reference(self,zp):
        self.zoom_panel=zp

    def update_circles_by_annotation(self):
        self.apm.checked=[]
        for i in self.value_picker_ctrl.value_pickers:
            if i.m_checkBox1.IsChecked()==True:
                self.apm.checked.append((i.value,i.clr,i.size))

        for i in self.leaf_coords:
            self.leaf_coords[i]['drawn']=False
            self.leaf_coords[i]['color']=None
            self.leaf_coords[i]['size']=None
            # i['node_annotation']

        all_taxa=self.annotation.get_EFDIDs_grouped_by(self.annotation.selected_annotation_field)
        for i in self.apm.checked:
            tx=all_taxa[i[0]]

            for j in tx:
                self.leaf_coords[j]['drawn']=True
                self.leaf_coords[j]['color']=i[1]
                self.leaf_coords[j]['annotation']=i[0]
                self.leaf_coords[j]['size']=i[2]
        self.get_circle_sets_by_color()

    def get_circle_sets_by_color(self):
        '''
        this is the final helper function for the circle drawing that gets a bunch of (color, list of coordinates) pairs
        :return:
        '''
        cols={}
        for i in self.leaf_coords:
            a=self.leaf_coords[i]
            if a['drawn']==True:
                if a['color'] in cols.keys():
                    cols[a['color']].append((a['x'],a['size']))
                else:
                    cols[a['color']]=[(a['x'],a['size'])]
        self.circle_sets_by_color=cols
        return cols

    def import_tree(self,path):
        # if path<>None:
            # self.tree_file=path
            # self.apm.tree_file=path

        self.image_frame.set_status("Importing Tree")
        self.buffered_window.import_new_tree(path)
        self.buffered_window.UpdateDrawing()
        # self.apm.initialize_tree()
        # self.image_frame.set_status("Calculating Max Dimensions")
        # self.max_data_dims=self.apm.rp.get_max_dims()
        # self.view_range=self.max_data_dims
        self.image_frame.set_status("Ready")

    def import_annotation(self,ann_path):
        node_labs = set(self.buffered_window.radial_phylogram.node_labels.keys())
        self.annotation = trman.AnnotationData(ann_path,node_labs)
        self.annotation_fields = self.annotation.headers

        # OLD:
        # self.annotation=trman.SfldAnnotationData(ann_path)
        # self.apm.initialize_annotation(ann_path)
        # self.annotation_fields=self.annotation.annotation_fields

    def unload_all(self):
        # self.apm=None
        # self.apm=trman.AnnotatedPhylogramModel()
        # self.value_picker_ctrl.clear_all()
        # self.image_frame.control_panel
        self.annotation=None
        self.buffered_window.radial_phylogram=None

    def trigger_refresh(self):
        if self.annotation is not None:
                cols = self.get_circle_sets_by_color()
        self.buffered_window.UpdateDrawing()

        # self.image_frame.get_current_tree_image()
        # if self.apm.state_node_annotation_loaded==True:
        #     self.image_frame.draw_circles()
        # self.image_frame.img_panel.Refresh()

    def trigger_annotation_picker_refresh(self):
        self.image_frame.control_panel.populate_annotation_values()
        pass

    def save_image(self,tgt_path):
        # self.image_frame.save_dc_to_bitmap(tgt_path)
        self.buffered_window.SaveToFile(tgt_path)

    def get_current_bitmap(self):
        return self.image_frame.current_bitmap

    def view_layout_main_frame(self):
        self.image_frame.control_panel.Layout()

class SEPPController():
    __metaclass__ = Singleton
    def __init__(self,sepp_output_file=None,sepp_annotation_file=None):
        self.sepp_output_file=sepp_output_file
        self.SeppValuePickerCtrl_ref=None

        self.sepp_annotation_file=sepp_annotation_file
        self.sepp_ann_dict={}
        self.show_all_values=False

        self.active_annotation_field=None
        self.active_unique_annotation_values=set([])
        self.active_unique_annotation_values_list=[]
        self.filter1_field=None
        self.filter1_options=set([])
        self.filter1_values=set([])
        self.filter2_field=None
        self.filter2_options=set([])
        self.filter2_values=set([])
        self.selected_annotation_values=set([])
        self.isfloat = False


    def set_bufferedwindow_reference(self,bw_ref):
        self.bw_ref=bw_ref
        self.ctrl_panel = bw_ref.parent.control_panel

    def initialize_sepp_json(self, sof=None):
        filter_vals = set(self.bw_ref.radial_phylogram.node_labels.keys())
        if sof is not None:
            self.sepp_output_file=sof
        sof=open(self.sepp_output_file,'r')
        self.json_str=sof.read()
        sof.close()
        self.myjson = json.loads(self.json_str)
        self.placements={}
        self.all_placements={}
        ins = 0
        not_in = 0
        if filter_vals is None:
            for i in self.myjson['placements']:
                for j in i['nm']:
                    if isinstance(j,list):
                        self.all_placements[j[0]]=i['p']
                        # get the one with the largest probability:
                        self.placements[j[0]]=reduce(lambda x,y: x if x[2] > y[2] else y, i['p'])

                    else:
                        self.all_placements[j] = i['p']
                        self.placements[j] = reduce(lambda x,y: x if x[2] > y[2] else y, i['p'])
        else:
            for i in self.myjson['placements']:
                if str(i['p'][0][0]) in filter_vals:
                    ins+=1
                    for j in i['nm']:
                        if isinstance(j,list):
                            self.all_placements[j[0]]=i['p']
                            self.placements[j[0]]=reduce(lambda x,y: x if x[2] > y[2] else y, i['p'])
                        else:
                            self.all_placements[j] = i['p']
                            self.placements[j] = reduce(lambda x,y: x if x[2] > y[2] else y, i['p'])
                else:
                    not_in +=0
                    # print i['nm']
                    # print i['p'][0][0]
        print "not ins are: %s" % not_in
        print "ins are: %s" % ins

        self.get_reference_tree_locations()

    def get_reference_tree_locations(self):
        print "making reference tree node point hash table..."
        self.ref_tree_point_lookup={}
        for i in self.bw_ref.radial_phylogram.myt.preorder_node_iter():
            if i.parent_node is not None:
                self.ref_tree_point_lookup[i.label]=(i.edge.length,i.edge.viewer_edge.head_x, i.edge.viewer_edge.tail_x)
        print "...done making reference tree node point hash table"

    def initialize_sepp_annotation(self,safpath=None,keycol=0):
        if safpath is not None:
            self.sepp_annotation_file=safpath
        saf=open(self.sepp_annotation_file,'r')
        self.saf_headers=saf.readline().strip().split('\t')
        # k=0
        for i in saf:
            ln = i.strip().split('\t')
            self.sepp_ann_dict[ln[keycol]]=tuple(ln)
            # k+=1
        # print k
        print len(self.sepp_ann_dict)

        saf.close()

    def load_filter1(self,header):
        f1_vals=[]
        print "getting values for header %s" % header
        self.filter1_field=header
        if self.filter1_field=='(none)':
            self.filter1_options = set([])
            self.filter1_values = set([])
        else:
            f1_col = self.saf_headers.index(header)
            for i in self.sepp_ann_dict.values():
                f1_vals.append(i[f1_col])

        self.filter1_options=set(f1_vals)
        return self.filter1_options

    def load_filter2(self,header):
        f2_vals=[]
        print "getting values for header %s" % header
        self.filter2_field=header
        if self.filter2_field=='(none)':
            self.filter2_options = set([])
            self.filter2_values = set([])
        else:
            f2_col = self.saf_headers.index(header)
            f1_col = self.saf_headers.index(self.filter1_field)
            for i in self.sepp_ann_dict.values():
                if len(self.filter1_values)==0 or i[f1_col] in self.filter1_values:
                    f2_vals.append(i[f2_col])

        self.filter2_options=set(f2_vals)
        return self.filter2_options

    def process_filter2(self,selections):
        if len(selections)==0:
            self.filter2_values=set([])
        else:
            self.filter2_values=set(selections)

    def process_filter1(self,selections):
        if len(selections)==0:
            self.filter1_values=set([])
        else:
            self.filter1_values=set(selections)

    def get_active_unique_annotation_values(self):
        if self.active_annotation_field is None or self.active_annotation_field=='':
            return None
        if self.active_unique_annotation_values is not None:
            del self.active_unique_annotation_values
        uav=[]
        ann_col = self.saf_headers.index(self.active_annotation_field)
        if self.filter1_field is not None:
            f1_col = self.saf_headers.index(self.filter1_field)
        if self.filter2_field is not None:
            f2_col = self.saf_headers.index(self.filter2_field)

        for i in self.sepp_ann_dict.keys():
            keep=True
            if self.filter1_field is not None and len(self.filter1_values)>0 and self.sepp_ann_dict[i][f1_col] not in self.filter1_values:
                keep = False
            elif self.filter2_field is not None and len(self.filter2_values)>0 and self.sepp_ann_dict[i][f2_col] not in self.filter2_values:
                keep = False
            if keep == True:
                uav.append(self.sepp_ann_dict[i][ann_col])

        self.active_unique_annotation_values = set(uav)
        self.active_unique_annotation_values_list=uav

    def update_circles_by_continuous_annotation(self):
        self.sepp_draw_circles = []
        with_pendants = self.ctrl_panel.m_checkBox3.IsChecked()

        ann_col = self.saf_headers.index(self.active_annotation_field)
        vals_for_scale=[]
        vals_to_draw=[]

        if len(self.filter1_values) > 0:
            f1_col = self.saf_headers.index(self.filter1_field)
        else:
            f1_col = None
        if len(self.filter2_values) > 0:
            f2_col = self.saf_headers.index(self.filter2_field)
        else:
            f2_col = None
        for i in self.sepp_ann_dict.values():
            vals_for_scale.append(i[ann_col])
            keep = True
            if f1_col is not None and i[f1_col] not in self.filter1_values:
                keep = False
            if f2_col is not None and i[f2_col] not in self.filter2_values:
                keep = False

            if keep == True:
                vals_to_draw.append(i)

        self.SeppValuePickerCtrl_ref.three_color_scale.set_values(vals_for_scale)
        print vals_to_draw[0][ann_col]
        print self.SeppValuePickerCtrl_ref.three_color_scale.get_color(vals_to_draw[0][ann_col])

        for i in vals_to_draw:
            x0 = self.get_location_ex_pendant(i[0])
            x1 = self.get_location_with_pendant(i[0])

            if x0 is not None:
                clr = self.SeppValuePickerCtrl_ref.three_color_scale.get_color(i[ann_col])
                sz = self.SeppValuePickerCtrl_ref.value_pickers[0].size
                if with_pendants == True:
                    self.sepp_draw_circles.append((x1, clr[0], clr[1], clr[2], sz, None))
                    self.bw_ref.ExtraDrawSegments.append((x1, x0, clr))
                else:
                    self.sepp_draw_circles.append((x0, clr[0], clr[1], clr[2], sz, None))

        self.bw_ref.SeppDrawCircles = self.sepp_draw_circles


    def update_circles_by_annotation(self):
        if self.isfloat == True:
            self.update_circles_by_continuous_annotation()
            return

        self.selected_annotation_values = {}
        self.sepp_draw_circles=[]
        with_pendants=self.ctrl_panel.m_checkBox3.IsChecked()

        for i in self.SeppValuePickerCtrl_ref.value_pickers:
            if i.m_checkBox1.IsChecked() == True:
                self.selected_annotation_values[i.value]=(i.clr, i.size)

        ann_col = self.saf_headers.index(self.active_annotation_field)
        if len(self.filter1_values)>0:
            f1_col = self.saf_headers.index(self.filter1_field)
        else:
            f1_col = None
        if len(self.filter2_values)>0:
            f2_col = self.saf_headers.index(self.filter2_field)
        else:
            f2_col = None

        for i in self.sepp_ann_dict.values():
            keep=True
            if i[ann_col] not in self.selected_annotation_values.keys():
                keep = False
            if f1_col is not None and i[f1_col] not in self.filter1_values:
                keep = False
            if f2_col is not None and i[f2_col] not in self.filter2_values:
                keep = False

            if keep == True:
                # x = self.get_location_ex_pendant(i[0])
                if self.show_all_values==False:
                    x0 = self.get_location_ex_pendant(i[0])
                    x1 = self.get_location_with_pendant(i[0])

                    if x0 is not None:
                        clr = self.selected_annotation_values[i[ann_col]][0]
                        sz = self.selected_annotation_values[i[ann_col]][1]
                        if with_pendants==True:
                            self.sepp_draw_circles.append((x1,clr[0],clr[1],clr[2],sz,None))
                            self.bw_ref.ExtraDrawSegments.append((x1,x0,clr))
                        else:
                            self.sepp_draw_circles.append((x0,clr[0],clr[1],clr[2],sz,None))
                else:
                    # TODO: make it showable with pendant branches
                    x0 = self.get_all_locations_ex_pendant(i[0])
                    try:
                        places = self.all_placements[i[0]]
                        clr = self.selected_annotation_values[i[ann_col]][0]
                        sz = self.selected_annotation_values[i[ann_col]][1]

                        for pct in range(len(places)):
                            if x0[pct] is not None:
                                self.sepp_draw_circles.append((x0[pct],clr[0],clr[1],clr[2],float(sz)*(float(places[pct][2])**.5)))
                    except KeyError:
                        pass

        self.bw_ref.SeppDrawCircles = self.sepp_draw_circles

    def trigger_refresh(self):
        self.bw_ref.UpdateDrawing()

    def get_all_locations_ex_pendant(self,nm):
        if nm not in self.placements.keys():
            return None

        places = self.all_placements[nm]
        circles=[]

        for place in places:
            try:
                edgevals=self.ref_tree_point_lookup[str(place[0])]
                hx = edgevals[1]
                tx = edgevals[2]
                e_len = edgevals[0]
                if e_len==0:
                    circles.append(tx)
                else:
                    frac = place[3] / e_len
                    circles.append((frac * hx[0] + (1 - frac) * tx[0], frac * hx[1] + (1 - frac) * tx[1]))
            except KeyError:
                circles.append(None)
        return circles


    def get_location_ex_pendant(self,nm):
        if nm not in self.placements.keys():
            # print "%s not in tree as shown" % nm
            return None

        place = self.placements[nm]
        # print nm
        # print place
        # nd=self.bw_ref.radial_phylogram.myt.find_node_with_label(str(place[0]))
        try:
            edgevals=self.ref_tree_point_lookup[str(place[0])]
        except KeyError:
            return None

        # hx = nd.edge.viewer_edge.head_x
        # tx = nd.edge.viewer_edge.tail_x
        hx = edgevals[1]
        tx = edgevals[2]
        e_len = edgevals[0]
        if e_len==0:
            return tx
        else:
            frac = place[3] / e_len
            circ_x = (frac * hx[0] + (1 - frac) * tx[0], frac * hx[1] + (1 - frac) * tx[1])
            return circ_x

    def get_location_with_pendant(self,nm):
        if nm not in self.placements.keys():
            print "%s not in tree as shown" % nm
            return None

        place = self.placements[nm]
        # print nm
        # print place
        # nd=self.bw_ref.radial_phylogram.myt.find_node_with_label(str(place[0]))
        try:
            edgevals=self.ref_tree_point_lookup[str(place[0])]
        except KeyError:
            return None

        # hx = nd.edge.viewer_edge.head_x
        # tx = nd.edge.viewer_edge.tail_x
        hx = edgevals[1]
        tx = edgevals[2]
        e_len = edgevals[0]
        if e_len==0:
            return tx
        else:
            frac = place[3] / e_len
            circ_x = (frac * hx[0] + (1 - frac) * tx[0], frac * hx[1] + (1 - frac) * tx[1])
            pen_x = (circ_x[0] + (hx[1]-tx[1])/e_len*place[4] / 4. ,circ_x[1]-(hx[0]-tx[0])/e_len*place[4] / 4.)
            # pen_x = (pen_x[0], pen_x[1])
            return pen_x

class AlignmentController(Controller):
    # __metaclass__ = Singleton
    def __init__(self):
        Controller.__init__(self)
        # self.starting_pt = self.image_frame.
        self.image_frame=None

        #Drawing Properties:
        self.circle_size=None
        self.max_data_dims=None
        self.view_range=None

        #File Properties
        # self.tree_file=None
        # self.annotation_file=None

