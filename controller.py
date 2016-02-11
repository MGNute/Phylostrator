__author__ = 'Michael'
import tree_manipulator as trman


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

class Controller():
    __metaclass__ = Singleton
    def __init__(self):
        self.apm=trman.AnnotatedPhylogramModel()
        self.current_uniques=[]
        self.value_picker_ctrl=None

        #Drawing Properties:
        self.circle_size=None
        self.max_data_dims=None
        self.view_range=None

        #File Properties
        # self.tree_file=None
        # self.annotation_file=None

    def save_model_to_file(self):
        #TODO: implement this
        self.apm.last_circle_size=self.circle_size
        self.apm.last_view_range=None
        # save the thing...
        pass

    def get_relevent_data_from_model(self):
        print "getting relevant data from model"
        self.max_data_dims=self.apm.rp.get_max_dims()
        print "getting leaf coordinate data copy"
        self.leaf_coords=self.apm.rp.leaf_node_coords
        print "getting the node_annotation fields"
        self.annotation_fields=self.apm.node_annotation.annotation_fields

    def set_ValuePickerCtrl_reference(self,vpc_pointer):
        self.value_picker_ctrl=vpc_pointer

    def set_ImageFrame_referenece(self,img_frame):
        self.image_frame=img_frame

    def update_cirlces_by_annotation(self):
        self.apm.checked=[]
        for i in self.value_picker_ctrl.value_pickers:
            if i.m_checkBox1.IsChecked()==True:
                self.apm.checked.append((i.value,i.clr,i.size))

        for i in self.leaf_coords:
            self.leaf_coords[i]['drawn']=False
            self.leaf_coords[i]['color']=None
            self.leaf_coords[i]['size']=None
            # i['node_annotation']

        all_taxa=self.apm.node_annotation.get_EFDIDs_grouped_by(self.apm.node_annotation_level)
        for i in self.apm.checked:
            tx=all_taxa[i[0]]

            for j in tx:
                self.leaf_coords[j]['drawn']=True
                self.leaf_coords[j]['color']=i[1]
                self.leaf_coords[j]['annotation']=i[0]
                self.leaf_coords[j]['size']=i[2]

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
        return cols

    def import_tree(self,path=None):
        if path<>None:
            # self.tree_file=path
            self.apm.tree_file=path

        self.image_frame.set_status("Importing Tree")
        self.apm.initialize_tree()
        self.image_frame.set_status("Calculating Max Dimensions")
        self.max_data_dims=self.apm.rp.get_max_dims()
        self.view_range=self.max_data_dims
        self.image_frame.set_status("Ready")

    def import_annotation(self,ann_path):
        self.apm.initialize_annotation(ann_path)
        self.annotation_fields=self.apm.node_annotation.annotation_fields

    def unload_all(self):
        self.apm=None
        self.apm=trman.AnnotatedPhylogramModel()
        self.value_picker_ctrl.clear_all()
        # self.image_frame.control_panel


    def trigger_refresh(self):
        self.image_frame.get_current_tree_image()
        if self.apm.state_node_annotation_loaded==True:
            self.image_frame.draw_circles()
        self.image_frame.img_panel.Refresh()

    def trigger_annotation_picker_refresh(self):
        self.image_frame.control_panel.populate_annotation_values()
        pass

    def save_image(self,tgt_path):
        self.image_frame.save_dc_to_bitmap(tgt_path)

    def get_current_bitmap(self):
        return self.image_frame.current_bitmap

    def view_layout_main_frame(self):
        self.image_frame.control_panel.Layout()

