import os, threading, sys
import wx, cairo, math
import wx.lib.scrolledpanel
from align_ctrl import *
from alignment import *
from utilities import *
import view_classes

class AlignmentControlPanel(WxfbAlignmentControlPanel):
    image_path = None
    ref_aln_path = None
    tree_path = None
    colors = {'A':None, 'C':None, 'G': None, 'T':None, 'U':None}
    annotation_dict = None

    #image borders:
    b_top=None
    b_bottom = None
    b_left = None
    b_right=None

    # image_parameters
    phylo_line_width = 1
    aln_start_col = 1
    aln_num_cols = 100
    gappy_threshold = 0.0

    def __init__(self,parent):
        WxfbAlignmentControlPanel.__init__(self,parent)
        self.image_frame = AlignmentImageFrame(self)
        self.image_frame.Show()
        self.cairo_drawer = CairoAlignmentDrawer()
        self.aln = None

    def import_alignment_and_tree( self, event = None):
        ap = self.m_AlnFile.GetPath()
        tp = self.m_TreeFile.GetPath()
        print ap
        print tp
        # self.aln = MultipleSequenceAlignment(refpath=ap,treepath=tp,generic_coords=True)
        self.aln = LightMutlipleSequenceAlignment(refpath=ap, treepath=tp, generic_coords=True)
        # self.m_textAlnLength.SetValue(str(len(self.aln.msa_cols)))
        self.m_textAlnLength.SetValue(str(self.aln.reflen))
        self.m_textAlnNumTaxa.SetValue(str(self.aln.numtaxa ))

        if self.m_AnnotationFile.GetPath() is not None and self.m_AnnotationFile.GetPath()<>'':
            self.parse_annotation_file()
            self.prepare_annotation_colorpickers()
            self.populate_annotation_values()
        else:
            self.annotation_dict={}
            for i in self.aln.ref.keys():
                self.annotation_dict[i]=i

    def prepare_annotation_colorpickers(self, event=None):
        self.value_picker_panel = wx.lib.scrolledpanel.ScrolledPanel(self.m_panel3, wx.ID_ANY, wx.DefaultPosition,
                                                                     wx.DefaultSize, 0)
        self.value_picker_panel.SetAutoLayout(1)
        self.value_picker = AlnValuePickerControl(self.value_picker_panel, wx.ID_ANY, wx.DefaultPosition,
                                                            wx.DefaultSize, wx.SUNKEN_BORDER)
        self.value_picker_sizer = self.m_panel3.GetSizer()
        self.value_picker_panel.EnableScrolling(False, True)

        self.value_picker_panel.SetSizer(self.value_picker)
        self.value_picker_panel.Layout()
        self.value_picker.Fit(self.value_picker_panel)
        self.value_picker_sizer.Add(self.value_picker_panel, 1, wx.EXPAND, 0)
        self.m_panel3.Layout()
        self.value_picker_sizer.Fit(self.m_panel3)
        # self.m_panel2.Layout()
        # self.m_panel2.Update()

    def populate_annotation_values(self,event=None):
        if self.m_AnnotationFile.GetPath() is not None and self.m_AnnotationFile.GetPath()<>'':
            unqs = list(set(self.annotation_dict.values()))
            cts = {}
            for i in unqs:
                cts[i]=0
            for i in self.annotation_dict.values():
                cts[i]+=1
            cts_list = [0,]*len(unqs)
            for i in range(len(unqs)):
                cts_list[i]=cts[unqs[i]]
            vals = []
            for i in range(len(unqs)):
                mind = cts_list.index(max(cts_list))
                vals.append(unqs.pop(mind))
                cts_list.pop(mind)
            self.value_picker.set_values(vals)
            self.value_picker_panel.SetupScrolling(False,True)
            self.m_panel2.Layout()
            # self.m_panel3.Update()

        else:
            print "no annotation selected, so no values have been populated"

    def notify_redraw(self,event=None):
        print "annotation drawing not yet implemented"

    def set_output_path( self, event =None):
        fn = self.m_textCairoImageFile.GetValue()
        if fn[-4:]<>".png":
            fn = fn + '.png'
        self.image_path = os.path.join(self.m_textCairoImgFolder.GetPath(),fn)

    def set_colors(self):
        cA = self.m_colourA.GetColour().Get()
        cC = self.m_colourC.GetColour().Get()
        cG = self.m_colourG.GetColour().Get()
        cT = self.m_colourT.GetColour().Get()
        aA = float(self.m_alphaA.GetValue())
        aC = float(self.m_alphaC.GetValue())
        aG = float(self.m_alphaG.GetValue())
        aT = float(self.m_alphaT.GetValue())
        self.colors['A']=(float(cA[0])/255.0, float(cA[1])/255.0, float(cA[2])/255.0, aA)
        self.colors['C'] = (float(cC[0]) / 255.0, float(cC[1]) / 255.0, float(cC[2]) / 255.0, aC)
        self.colors['G'] = (float(cG[0]) / 255.0, float(cG[1]) / 255.0, float(cG[2]) / 255.0, aG)
        self.colors['T'] = (float(cT[0]) / 255.0, float(cT[1]) / 255.0, float(cT[2]) / 255.0, aT)
        self.colors['U'] = (float(cT[0]) / 255.0, float(cT[1]) / 255.0, float(cT[2]) / 255.0, aT)
        self.colors['N'] = (.8, .8, .8, .8)
        self.colors['M'] = (.4, .4, .4, .4)

    def set_cairo_settings(self):
        self.set_colors()
        try:
            w = int(self.m_textCairoImgWidth.GetValue())
            self.cairo_drawer.W = w
        except:
            print "%s won't convert to an integer..." % self.m_textCairoImgWidth.GetValue()

        try:
            h = int(self.m_textCairoImgHeight.GetValue())
            self.cairo_drawer.H = h
        except:
            print "%s won't convert to an integer..." % self.m_textCairoImgHeight.GetValue()

        self.pct_to_alignment = float(self.m_textPctWidthToAlignment.GetValue()) / 100.0
        self.pct_to_phylogeny = float(self.m_textPctWidthToPhylogeny.GetValue()) / 100.0
        self.pct_to_names = 1-self.pct_to_alignment - self.pct_to_phylogeny
        self.n = self.aln.numtaxa

        self.b_bottom=float(self.m_borderBottom.GetValue())
        self.b_top = float(self.m_borderTop.GetValue())
        self.b_left = float(self.m_borderLeft.GetValue())
        self.b_right = float(self.m_borderRight.GetValue())

        self.phylo_line_width = float(self.m_textPhylogenyLineWidth.GetValue())
        self.aln_start_col = int(self.m_textStartColumn.GetValue())
        self.aln_num_cols = int(self.m_textNumColumns.GetValue())


        # Stuff in External Ojbects:
        self.set_output_path()
        self.image_frame.path = self.image_path
        self.cairo_drawer.path = self.image_path
        print '''
        Active Cairo Settings:
           -Size: %(W)s, %(H)s
           -Path: %(path)s
        ''' % self.cairo_drawer.get_settings()

    def on_batch_click( self, event=None ):
        # tot_cols = len(self.aln.msa_cols)
        tot_cols = int(self.aln.active_cols.shape[0])
        numcols = int(self.m_textNumColumns.GetValue())
        num_images = int(math.ceil(float(tot_cols)/float(numcols)))
        fn_pref = self.m_textCairoImageFile.GetValue()
        for i in range(num_images):
            st_col = str(1+numcols*i)
            self.m_textStartColumn.SetValue(st_col)
            self.m_textCairoImageFile.SetValue(fn_pref + '_start_' + st_col + '_n_' + str(numcols))
            self.draw_cairo()

    def on_mask_gappy_columns( self, event = None ):
        if self.m_checkBox1.IsChecked():
            self.m_textCtrl20.Enable()
            self.m_staticText231.Enable()
            self.m_textAlnLength1.Enable()
            self.gappy_threshold = float(self.m_textCtrl20.GetValue()) / 100
        else:
            self.m_textCtrl20.Disable()
            self.m_staticText231.Disable()
            self.m_textAlnLength1.Disable()
            self.gappy_threshold = 0.0

        # if self.m_textCtrl20.IsEnabled:
        #     print "gappy cols percent text control enabled"
        # else:
        #     print "gappy cols percent text control disabled"

        self.aln.set_active_cols(self.gappy_threshold)

        if self.m_checkBox1.IsChecked():
            self.m_textAlnLength1.SetValue(str(self.aln.active_cols.shape[0]))
        else:
            self.m_textAlnLength1.SetValue("(unmasked)")

    def on_change_gappy_threshold( self, event = None):
        try:
            self.gappy_threshold =float(self.m_textCtrl20.GetValue())
            print "setting gappy threshold to %s" % self.gappy_threshold
        except:
            print "percent masked must reconcile to a decimal number"
            self.m_textCtrl20.SetValue("0.0")

        self.aln.set_active_cols(self.gappy_threshold)
        if self.m_textCtrl20.IsEnabled:
            self.m_textAlnLength1.SetValue(str(self.aln.active_cols.shape[0]))
        else:
            self.m_textAlnLength1.SetValue("(unmasked)")


    def call_draw_cairo_thread(self):
        t=threading.Thread(target=self.draw_cairo)
        t.start()

    def show_viewer(self):
        self.image_frame.Show()

    def draw_cairo( self, event=None):
        wx.CallAfter(self.show_viewer)
        print 'getting settings ready...'
        self.set_cairo_settings()
        self.cairo_drawer.init_graphic()
        b_v = self.b_top + self.b_bottom
        b_h = self.b_right + self.b_left
        segs = []
        # actual_num_cols=min(self.aln_num_cols,len(self.aln.msa_cols)-self.aln_start_col)
        # actual_num_cols = min(self.aln_num_cols, self.aln.reflen - self.aln_start_col)
        actual_num_cols = min(self.aln_num_cols, int(self.aln.active_cols.shape[0]) - self.aln_start_col)

        # Draw the Phylogeny
        for i in self.aln.segment_endpoints:
            segs.append((self.b_left+(1.0-i[0])*(self.cairo_drawer.W-b_v)*self.pct_to_phylogeny,
                        self.b_top+i[1]*(self.cairo_drawer.H-b_h),
                         self.b_left + (1.0-i[2]) * (self.cairo_drawer.W - b_v)*self.pct_to_phylogeny,
                         self.b_top + i[3] * (self.cairo_drawer.H - b_h)))

        # Draw the Alignment Characters (TODO-make it so we can scroll rather than just having to make a bigger and bigger png?
        left_limit = self.b_left+self.pct_to_phylogeny*(self.cairo_drawer.W-b_h)+float(self.m_textAlignmentPhylogenySpacerWidth.GetValue())
        right_limit = left_limit - float(self.m_textAlignmentPhylogenySpacerWidth.GetValue()) + (self.cairo_drawer.W-b_h)*self.pct_to_alignment
        print "leftlimit %s, rightlimit %s" % (left_limit,right_limit)
        top_limit = self.b_top
        bot_limit = self.cairo_drawer.H - self.b_bottom
        h_spacing = (right_limit-left_limit)/self.aln_num_cols
        v_spacing = (bot_limit - top_limit)/self.n

        rect_groups={'A':[], 'C':[], 'G':[], 'T':[], 'U':[], 'M':[], 'N':[]}

        # for i in range(actual_num_cols):
        #     col = self.aln.msa_cols[self.aln_start_col+i-1]
        #     for j in col.chars.keys():
        #         chval = col.chars[j][2]
        #         if chval not in rect_groups.keys():
        #             rect_groups[chval]=[]
        #             self.colors[chval] = (1.0,1.0,1.0,1.0)
        #         rect_groups[chval].append((left_limit+i*h_spacing,top_limit+j*v_spacing,h_spacing,v_spacing))

        for i in range(actual_num_cols):
            # col = self.aln.msa_cols[self.aln_start_col+i-1]
            # colnum = self.aln_start_col+i-1
            colnum = self.aln.active_cols[self.aln_start_col + i - 1]
            for j in self.aln.ref.keys():
                no = self.aln.node_order_lookup[j]
                chval = self.aln.ref[j][colnum]
                if chval not in rect_groups.keys():
                    rect_groups[chval]=[]
                    self.colors[chval] = (1.0,1.0,1.0,1.0)
                rect_groups[chval].append((left_limit+i*h_spacing,top_limit+no*v_spacing,h_spacing,v_spacing))

        for i in rect_groups.keys():
            clr = self.colors[i]
            self.cairo_drawer.draw_boxes_one_color(rect_groups[i],clr)

        grouping = {}
        for i in self.value_picker.values:
            grouping[i]=[]

        # Draw the Text Names:
        if self.annotation_dict is None:
            for i in range(self.n):
                lab=self.aln.node_order[i]
                self.cairo_drawer.draw_text((right_limit+2,top_limit+(i+1)*v_spacing),lab)
        else:
            for i in range(self.n):
                lab=self.aln.node_order[i]
                self.cairo_drawer.draw_text((right_limit+2,top_limit+(i+1)*v_spacing),self.annotation_dict[lab])
                grouping[self.annotation_dict[lab]].append(i)

        self.draw_annotation(grouping, top_limit, right_limit, v_spacing)

        print 'Drawing the image file'
        self.cairo_drawer.draw_line_set(segs,self.phylo_line_width)

        self.cairo_drawer.finish_graphic()
        self.image_frame.refresh_image()
        print 'Done making graphic'

    def draw_annotation(self,grouping, top_limit, right_limit, v_spacing):
        for k in grouping.keys():
            # circs=[]
            boxs=[]
            if self.value_picker.checked[k]==True:
                clr=self.value_picker.colors[k]
                cf = (clr[0]/255., clr[1]/255., clr[2]/255., .5)
                for j in grouping[k]:
                    # circs.append((3,top_limit+(j+1)*v_spacing+v_spacing/2., v_spacing/3.))
                    boxs.append((3,top_limit+(j+1)*v_spacing,self.cairo_drawer.W*self.pct_to_phylogeny-3,v_spacing))
                # self.cairo_drawer.draw_circles_one_color(circs,cf)
                self.cairo_drawer.draw_boxes_one_color(boxs,cf)



    def parse_annotation_file(self):
        self.annotation_dict={}
        if self.m_AnnotationFile.GetPath() <> None and os.path.exists(self.m_AnnotationFile.GetPath()):
            f=open(self.m_AnnotationFile.GetPath())
            for line in f:
                if len(line)>0:
                    a= line.strip().split('\t')
                    self.annotation_dict[a[0]]='--'.join(a[1:2])
            f.close()
        else:
            self.annotation_dict=None

class AlnValuePickerControl(wx.BoxSizer):
    def __init__(self,parent,*args):
        wx.BoxSizer.__init__(self,wx.VERTICAL)
        self.parent=parent
        self.value_pickers=[]
        self.values=None
        self.colors=None

    # def notify_redraw(self):
    #     pass

    def clear_all(self):
        self.Clear(True)
        self.values=[]
        self.value_pickers=[]

    def set_all_sizes(self,size):
        if len(self.value_pickers)>0:
            for i in self.value_pickers:
                i.set_size(size)
        self.value_pickers[0].process_size_change()

    def select_all(self):
        if len(self.value_pickers)>0:
            for i in self.value_pickers:
                i.m_checkBox1.SetValue(True)
        self.value_pickers[0].process_annotationvalue_check()

    def unselect_all(self):
        if len(self.value_pickers)>0:
            for i in self.value_pickers:
                i.m_checkBox1.SetValue(False)
        self.value_pickers[0].process_annotationvalue_check()

    def set_values(self,vals=None):
        self.clear_all()
        if vals != None:
            self.values=vals

        k=0

        self.colors={}
        self.checked={}
        for i in self.values:
            if k>=len(colors):
                clr=get_random_color()
            else:
                clr=colors[k]
                k+=1

            self.colors[i]= clr
            a = AlnValuePicker(self.parent, i, clr, val_ctrl=self)
            self.checked[i] = False
            self.Add(a,0, wx.EXPAND, 5)
            self.value_pickers.append(a)

        self.add_final_spacer()

    def notify_colorchange(self, val, clr):
        self.colors[val]=clr

    def notify_checkmark(self,val, ischecked):
        self.checked[val] = ischecked

    def update_all_checked_and_colors(self):
        for i in self.value_pickers:
            self.colors[i.value]=i.clr
            self.checked[i.value]=i.m_checkBox1.IsChecked()

    def add_final_spacer(self):
        bSizer15 = wx.BoxSizer( wx.VERTICAL )
        bSizer15.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        self.Add( bSizer15, 1, wx.EXPAND, 5 )

    def move_to_bottom(self,val):
        val_temps=[]
        for i in self.value_pickers:
            args={'parent':self.parent, 'clr':i.clr, 'value':i.value, 'sz':i.size, 'checked':i.m_checkBox1.GetValue(), 'val_ctrl':self}
            val_temps.append(args)
        for v in val_temps:
            # print v
            if v['value']==val:
                ind=val_temps.index(v)
                tmp = val_temps.pop(ind)
                val_temps.append(tmp)
        self.load_values(val_temps)

    def load_values(self,val_temps):

        self.clear_all()
        for i in val_temps:
            # vp=self.ValuePicker(**i)
            vp = AlnValuePicker(**i)
            self.Add(vp,0, wx.EXPAND,5)
            self.value_pickers.append(vp)
        self.add_final_spacer()
        self.Layout()

class AlnValuePicker(wx.BoxSizer):
    def __init__(self,parent=None, value=None,clr=None, sz=3, checked=False, val_ctrl=None):
        self.parent=parent
        self.value_picker_control=val_ctrl
        self.value=value
        self.clr=clr
        self.size=sz
        wx.BoxSizer.__init__(self,wx.HORIZONTAL)
        self.m_checkBox1 = wx.CheckBox(parent, wx.ID_ANY, value, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox1.SetValue(checked)
        self.Add( self.m_checkBox1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_colourPicker1 = wx.ColourPickerCtrl(parent, wx.ID_ANY, wx.Colour(clr[0],clr[1],clr[2]), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        self.Add( self.m_colourPicker1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_spinCtrl=wx.SpinCtrl(parent, initial=self.size)
        self.m_spinCtrl.SetMaxSize(wx.Size(50,-1))
        self.Add(self.m_spinCtrl,0,wx.ALL,5)

        self.m_spinCtrl.Bind(wx.EVT_SPINCTRL,self.process_size_change)

        self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.process_annotationvalue_check )
        self.m_colourPicker1.Bind( wx.EVT_COLOURPICKER_CHANGED, self.process_color_change )

    def process_annotationvalue_check(self,event=None):
        self.value_picker_control.notify_checkmark(self.value, self.m_checkBox1.IsChecked())
        self.parent.GetParent().GetParent().GetParent().GetParent().notify_redraw()

    def process_color_change(self,event=None):
        newcolor=self.m_colourPicker1.GetColour()
        self.clr=newcolor.Get()
        self.value_picker_control.notify_colorchange(self.value, self.clr)
        self.parent.GetParent().GetParent().GetParent().GetParent().notify_redraw()

    def process_size_change(self,event=None):
        print "size not used in this implementation"
        self.size=int(self.m_spinCtrl.GetValue())
        # self.c.update_circles_by_annotation()
        # self.c.trigger_refresh()

    def set_size(self,size):
        self.size=int(size)
        self.m_spinCtrl.SetValue(self.size)

class AlignmentImageFrame(WxfbAlignmentImageFrame):
    path=None
    def __init__(self,parent):
        WxfbAlignmentImageFrame.__init__(self,parent)
        self.Maximize()

    def load(self,path):
        self.path=path
        self.refresh_image()

    def refresh_image( self, event=None ):
        if self.path <> None and os.path.exists(self.path):
            self.m_htmlWin1.LoadFile(self.path)
        else:
            print 'The file %s does not exist...' % self.path


class CairoAlignmentDrawer():
    W=None
    H=None
    path='resources/test_alignment.png'
    colors={
        'A':None,
        'C':None,
        'G':None,
        'T':None,
        'U':None,
        'M':None,
        'N':None
    }
    surf=None
    ctx=None

    def __init__(self,path=None):
        if path is not None:
            self.path=path
        pass

    def get_settings(self):
        args={}
        args['W'] = self.W
        args['H'] = self.H
        args['path'] = self.path

        return args

    def init_graphic(self):
        if self.surf is not None:
            del self.surf
        if self.ctx is not None:
            del self.ctx
        self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.W, self.H)
        self.ctx = cairo.Context(self.surf)
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.W, self.H)
        self.ctx.fill()

    def draw_box(self,top_left,size,color):
        self.ctx.set_source_rgba(*color)
        self.ctx.rectangle(top_left[0],top_left[1],size[0],size[1])
        self.ctx.fill()

    def draw_text(self,bottom_left,text):
        # print 'drawing text \'%s\' at the point %s' %(text,str(bottom_left))
        self.ctx.set_source_rgba(0,0,0,1)
        self.ctx.move_to(*bottom_left)
        self.ctx.show_text(text)

    def draw_circles_one_color(self,circs, color):
        '''
        circs must be a list of triples of the form (x, y, rad) all in floating points
        '''
        self.ctx.set_source_rgba(*color)
        for c in circs:
            self.ctx.new_sub_path()
            self.ctx.arc(c[0], c[1], c[2], 0, 2*math.pi)
        self.ctx.fill()

    def draw_boxes_one_color(self,boxes,color):
        '''
        Draws many boxes that will be all of the same color.
        :param boxes: list of 4-tuples with (x,y,w,h) coordinates
        :param color: RGBA 4-tuple
        :return:
        '''
        self.ctx.new_path()
        self.ctx.set_source_rgba(*color)
        ct =0
        for i in boxes:
            self.ctx.rectangle(*i)
            ct +=1
            if ct % 500 ==0:
                self.ctx.fill()
        self.ctx.fill()

    def draw_line_set(self,line_set,line_width=None):
        '''
        Draws a set of lines by way of sub-paths for every (x0, y0, x1, y1) point in the list
        :param line_set: [(x0,y0,x1,y1)_1,(x0,y0,x1,y1)_2, ...]

        '''
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.new_path()
        if line_width<>None:
            old_lw = self.ctx.get_line_width()
            self.ctx.set_line_width(line_width)

        for i in line_set:
            self.ctx.new_sub_path()
            self.ctx.move_to(i[0],i[1])
            self.ctx.line_to(i[2],i[3])
        self.ctx.stroke()
        self.ctx.set_line_width(old_lw)

    def finish_graphic(self):
        self.surf.write_to_png(self.path)

class AlignmentApp(wx.App):
    def OnInit(self):
        self.mainframe = AlignmentControlPanel(None)
        self.SetTopWindow(self.mainframe)
        self.mainframe.SetIcon(wx.Icon('resources/icnPhyloMain32.png'))
        self.mainframe.Show()
        return True

if __name__=='__main__':
    app = AlignmentApp()
    app.MainLoop()