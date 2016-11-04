import scripts

__author__ = 'Michael'

# from my_globals import *
import sfld_view
import view_classes
import controller
import wx
import wx.lib.scrolledpanel
import os.path
import utilities
import math

class MyApp(wx.App):
    def OnInit(self):
        self.mainframe = image_manager(None)
        self.SetTopWindow(self.mainframe)
        self.mainframe.SetIcon(wx.Icon('resources/icnPhyloMain32.png'))
        self.mainframe.Show()

        return True



class gui_manager(sfld_view.ctrlFrame):
    '''
    top level frame for this application
    '''
    tree_file=None
    annotation_file=None
    def __init__(self,parent):
        self.parent=parent
        sfld_view.ctrlFrame.__init__(self,parent)

        self.c=controller.Controller()
        self.sepp_c = controller.SEPPController()

        self.working_folder=None

        # self.cold_initialize()

        # self.initial_checks()

        self.value_picker_panel=wx.lib.scrolledpanel.ScrolledPanel(self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.value_picker_panel.SetAutoLayout(1)
        self.value_picker = view_classes.ValuePickerControl(self.value_picker_panel, wx.ID_ANY, wx.DefaultPosition,
                                                            wx.DefaultSize, wx.SUNKEN_BORDER)
        self.value_picker_sizer = self.m_panel5.GetSizer()
        self.value_picker_panel.EnableScrolling(False,True)

        self.value_picker_panel.SetSizer(self.value_picker)
        self.value_picker_panel.Layout()
        self.value_picker.Fit(self.value_picker_panel)
        self.value_picker_sizer.Add(self.value_picker_panel,1,wx.EXPAND,0)
        self.m_panel5.Layout()
        self.value_picker_sizer.Fit(self.m_panel5)


        self.sepp_value_picker_panel=wx.lib.scrolledpanel.ScrolledPanel(self.m_panel51, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.sepp_value_picker_panel.SetAutoLayout(1)
        self.sepp_value_picker= view_classes.SEPPValuePickerControl(self.sepp_value_picker_panel, wx.ID_ANY, wx.DefaultPosition,
                                                            wx.DefaultSize, wx.SUNKEN_BORDER)
        self.sepp_value_picker_sizer = self.m_panel51.GetSizer()
        self.sepp_value_picker_panel.EnableScrolling(False,True)
        self.sepp_value_picker_panel.SetSizer(self.sepp_value_picker)
        self.sepp_value_picker_panel.Layout()
        self.sepp_value_picker.Fit(self.sepp_value_picker_panel)
        self.sepp_value_picker_sizer.Add(self.sepp_value_picker_panel, 1, wx.EXPAND, 0)
        self.m_panel51.Layout()
        self.sepp_value_picker_sizer.Fit(self.m_panel51)

        self.c.circle_size=self.m_slider1.GetValue()
        self.layout_viewer_panel()
        self.Layout()
        self.MoveXY(100, 100)
        # self.MoveXY(1620,300)


        #TODO: This is just for the verstion where we want to do a cold initialize, otherwise have to make the image frame
        #    decide whether to show itself, etc...

        # self.image_frame=image_manager(self)
        # self.c.set_ImageFrame_referenece(self.image_frame)
        # self.image_frame.Show()

    def draw_circles( self, event=None ):
        self.sepp_c.update_circles_by_annotation()
        self.c.buffered_window.UpdateDrawing()

    def cold_initialize(self):
        self.set_file()
        self.set_annotation_file()
        self.import_tree()
        self.import_annotation()

    def populate_annotation_fields(self):
        # ONLY EXECUTE THIS ONCE THE ANNOTATION HAS BEEN LOADED
        # if self.c.apm.state_node_annotation_loaded==True:
        flds=self.c.annotation_fields
        self.m_ComboSelectedField.Clear()
        self.m_ComboSelectedField.AppendItems(flds)
        self.m_comboBox61.Clear()
        self.m_comboBox61.AppendItems(flds)
        self.m_comboBox51.Clear()
        self.m_comboBox51.AppendItems(flds)

        self.add_value_pickers()

        if 'Phylum' in flds:
            self.m_ComboSelectedField.SetValue('Phylum')
            self.populate_annotation_values()
        elif 'phylum' in flds:
            self.m_ComboSelectedField.SetValue('phylum')
            self.populate_annotation_values()

    def draw_text(self,event=None, text=None):
        raise NotImplementedError
        # if text == None:
        #     text = self.m_textCtrl4.GetValue()
        # self.parent.draw_text(text)

    def populate_annotation_values(self,event=None):
        fld = self.m_ComboSelectedField.GetValue()
        # self.c.node_annotation_level=fld
        # unqs = self.c.annotation.uniques[fld]
        self.c.annotation.selected_annotation_field=fld
        unqs=self.c.annotation.get_active_unique_annotation_values()

        self.value_picker.set_values(unqs)
        self.add_value_pickers()
        # self.m_panel5.SetSizer(self.value_picker)
        # self.value_picker_panel.Layout()
        # self.value_picker_sizer.Fit(self.m_panel5)
        # self.m_panel5.Fit()
        # self.m_panel5.Layout()
        # self.value_picker.FitInside(self.m_panel5)
        # self.m_panel4.Layout()
        self.c.set_ValuePickerCtrl_reference(self.value_picker)



    #
    # methods related to value picker
    #

    def add_value_pickers(self):
        # pass
        # self.m_panel5.SetSizer( self.value_picker)
        self.value_picker_panel.SetSizer(self.value_picker)
        # w,h = self.value_picker.GetMinSize()
        # self.value_picker_panel.SetVirtualSize((w,h))
        self.value_picker_panel.Layout()
        self.value_picker.Fit(self.value_picker_panel)
        # self.value_picker_panel.SetVirtualSize((w, h))
        self.value_picker_panel.FitInside()

        # self.m_panel5.Fit()
        # self.m_panel5.Layout()
        # self.value_picker_sizer.Fit(self.m_panel5)


        # self.value_picker.Fit(self.value_picker_panel)
        self.m_panel4.Layout()
        self.Layout()
        self.value_picker_panel.SetupScrolling()

    def valpicker_clear( self, event ):
        self.value_picker.clear_all()


    def valpicker_load( self, event ):
        # self.value_picker
        pass

    def load_filter1( self, event=None ):
        f1_field=self.m_comboBox51.GetValue()
        opts=self.c.annotation.load_filter1(f1_field)
        self.m_listBox31.SetItems(list(opts))

    def load_filter2( self, event=None ):
        f2_field=self.m_comboBox61.GetValue()
        opts=self.c.annotation.load_filter2(f2_field)
        self.m_listBox21.SetItems(list(opts))

    def process_filter1( self, event =None):
        filter1_selections=self.m_listBox31.GetSelections()
        filter1_items=self.m_listBox31.GetItems()
        strItems=[]
        for i in filter1_selections:
            strItems.append(filter1_items[i])
        self.c.annotation.process_filter1(strItems)
        self.populate_annotation_values()

    def process_filter2( self, event=None ):
        filter2_selections = self.m_listBox21.GetSelections()
        filter2_items = self.m_listBox21.GetItems()
        strItems=[]
        for i in filter2_selections:
            strItems.append(filter2_items[i])
        self.c.annotation.process_filter2(strItems)
        self.populate_annotation_values()


    #
    # methods related to SEPP value picker
    #
    def sepp_import_annotation( self, event=None ):
        self.sepp_c.set_bufferedwindow_reference(self.parent.img_panel)
        sjson = self.m_filePicker5.GetPath()
        sann = self.m_FilePicker_annotation1.GetPath()
        self.sepp_c.initialize_sepp_annotation(sann)
        self.sepp_c.initialize_sepp_json(sjson)

        self.m_ComboSelectedField1.Clear()
        self.m_comboBox6.Clear()
        self.m_comboBox5.Clear()
        self.m_comboBox5.Append('(none)')
        self.m_comboBox6.Append('(none)')
        for i in self.sepp_c.saf_headers:
            self.m_comboBox5.Append(i)
            self.m_comboBox6.Append(i)
            self.m_ComboSelectedField1.Append(i)
        print "done with import"

    def sepp_load_filter1( self, event=None ):
        f1_field=self.m_comboBox5.GetValue()
        opts=self.sepp_c.load_filter1(f1_field)
        print opts
        self.m_listBox3.SetItems(list(opts))
        pass

    def sepp_load_filter2( self, event=None ):
        f2_field=self.m_comboBox6.GetValue()
        opts=self.sepp_c.load_filter2(f2_field)
        print opts
        self.m_listBox2.SetItems(list(opts))


    def sepp_process_filter1( self, event=None ):
        filter1_selections=self.m_listBox3.GetSelections()
        # print filter1_selections
        filter1_items=self.m_listBox3.GetItems()
        strItems=[]
        for i in filter1_selections:
            strItems.append(filter1_items[i])
        self.sepp_c.process_filter1(strItems)
        self.sepp_populate_annotation_values()
        pass

    def sepp_process_filter2( self, event=None ):
        filter2_selections = self.m_listBox2.GetSelections()
        # print filter2_selections
        filter2_items = self.m_listBox2.GetItems()
        strItems=[]
        for i in filter2_selections:
            strItems.append(filter2_items[i])
        self.sepp_c.process_filter2(strItems)
        self.sepp_populate_annotation_values()
        pass

    def sepp_populate_annotation_values( self, event=None ):
        sepp_fld = self.m_ComboSelectedField1.GetValue()
        self.sepp_c.active_annotation_field=sepp_fld
        self.sepp_c.get_active_unique_annotation_values()
        unqs = self.sepp_c.active_unique_annotation_values
        self.sepp_c.isfloat = False
        if self.m_checkBox5.IsChecked():
            try:
                foo = float(unqs[0]) + float(unqs[1])
                self.sepp_c.isfloat = True
            except:
                self.sepp_c.isfloat = False

        if self.sepp_c.isfloat ==True:
            self.sepp_value_picker.set_color_scale(list(set(unqs)))
        else:
            if len(unqs)>50:
                print "this list has more than 50 elements, so we're not going to list them all. Try filtering down first"
                self.sepp_value_picker.set_values(unqs[0:30])
            else:
                self.sepp_value_picker.set_values(unqs)

        self.sepp_add_value_pickers()
        self.sepp_c.SeppValuePickerCtrl_ref=self.sepp_value_picker
        if self.sepp_c.isfloat==True:
            self.sepp_c.update_circles_by_annotation()
        pass

    def sepp_add_value_pickers(self,event=None):
        self.sepp_value_picker_panel.SetSizer(self.sepp_value_picker)
        self.sepp_value_picker_panel.Layout()
        self.sepp_value_picker.Fit(self.sepp_value_picker_panel)
        self.sepp_value_picker_panel.FitInside()
        self.m_panel41.Layout()
        self.Layout()
        self.sepp_value_picker_panel.SetupScrolling()


        pass

    def clear_extra_circles( self, event = None):
        self.c.buffered_window.SeppDrawCircles = None




    def initial_checks(self):
        if self.m_FilePicker_tree.GetTextCtrlValue()<>'':
            self.set_file(filepath=self.m_FilePicker_tree.GetTextCtrlValue())
        if self.m_FilePicker_annotation.GetTextCtrlValue()<>'':
            self.annotation_file=self.m_FilePicker_annotation.GetTextCtrlValue()

    def set_file( self, event=None, filepath=None):
        print "file changed"
        fo=''
        self.c.apm.tree_file=self.m_FilePicker_tree.GetPath()
        # print self.c.tree_file
        try:
            fo, fi = os.path.split(self.c.apm.tree_file)
        except:
            pass


    def on_show_legend_check( self, event=None ):
        if self.m_checkBox4.IsChecked():
            legend_data=[]
            for i in self.value_picker.value_pickers:
                if i.m_checkBox1.IsChecked():
                    legend_data.append((i.value, i.clr))
            W=int(self.m_textCtrl12.GetValue())
            H=int(self.m_textCtrl13.GetValue())
            self.c.buffered_window.LegendDrawData={
                'W': W,
                'H': H,
                'entries': legend_data
            }
        else:
            self.c.buffered_window.LegendDrawData=None
        self.c.buffered_window.UpdateDrawing()

    def move_legend( self, event=None ):
        self.c.buffered_window.LegendDrawData['W'] = int(self.m_textCtrl12.GetValue())
        self.c.buffered_window.LegendDrawData['H'] = int(self.m_textCtrl13.GetValue())
        self.c.buffered_window.UpdateDrawing()

    def set_working_folder(self,event=None):
        self.working_folder=self.m_dirPicker3.GetPath()
        self.txt_workingFolder.SetValue(self.working_folder)

    def set_annotation_file( self, event=None, filepath=None):
        self.annotation_file=self.m_FilePicker_annotation.GetPath()


    def SaveCurrentImage(self,event,tgt_path=None):
        tgt_file=self.m_textImageSaveTarget.GetValue()
        if tgt_path==None:
            tgt_path=os.path.join(self.working_folder,tgt_file)
        self.c.save_image(tgt_path)

    def reroot_above(self,event=None):
        self.c.buffered_window.reroot_above_active_edge()

    def rotate_clockwise( self, event=None ):
        self.c.buffered_window.pivot_clockwise


    def layout_viewer_panel(self):
        # self.m_panel6 = view_classes.ViewAreaSelectorPanel( self.viewer_panel, wx.ID_ANY, (1,50), wx.Size(500,300), style=wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
        # self.m_panel6.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        # self.m_panel6.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        # self.zoom_control = view_classes.zoom_rotation_ctrl( self.viewer_panel)
        self.make_viewer_panel_ojbect()
        self.m_panel9.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_panel9.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        mysizer= self.viewer_panel.GetSizer()
        mysizer.Add(self.m_panel9, 1, wx.EXPAND | wx.ALL, 5)
        # self.viewer_panel.Layout()
        # mysizer.Fit(self.viewer_panel)
        self.viewer_panel.Layout()
        self.viewer_panel.Refresh()
        mysizer.Fit(self.viewer_panel)
        # self.txtZoom = wx.StaticText()

    def make_viewer_panel_ojbect(self):
        self.m_panel9 = view_classes.ViewAreaSelectorPanel(self.viewer_panel, wx.ID_ANY, wx.DefaultPosition,
                                                           wx.DefaultSize, wx.TAB_TRAVERSAL)

    # def process_annotationvalue_check(self,event):
    #     checked=[]
    #     for i in self.value_picker.value_pickers:
    #         if i.m_checkBox1.IsChecked()==True:
    #             checked=(i.value, i.clr)
    #
    #     print checked

    def import_tree( self, event=None ):
        mytree=self.m_FilePicker_tree.GetPath()
        if mytree[-3:].lower()=='.rp':
            print "importing from picked file %s" % mytree
            import pickle
            fi = open(mytree,'r')
            self.c.buffered_window.radial_phylogram=pickle.load(fi)
            fi.close()
            self.c.buffered_window.MakeDrawData(False)
            self.c.buffered_window.UpdateDrawing()
        else:
            self.c.import_tree(mytree)

    def import_annotation( self, event=None ):
        self.set_annotation_file()
        self.c.import_annotation(self.annotation_file)

        # if self.c.apm.state_tree_loaded==True:
        self.c.get_relevent_data_from_model()
        self.populate_annotation_fields()
        # else:
        #     print "Tree not loaded, so no action taken."

    def trigger_redraw(self,event=None):
        self.c.buffered_window.MakeDrawData()
        self.c.circle_size=int(self.m_slider1.GetValue())
        self.c.trigger_refresh()

    def on_frame_close( self, event ):
        if event.CanVeto():
            event.Veto()
            self.Iconize()

    def adjust_rotation( self, event=None ):
        rot=self.m_textCtrl101.GetValue()
        fRot=int(rot)
        print "adjusting rotation to %s degrees" % fRot
        self.c.set_tree_rotation(fRot)
        self.m_panel9.set_global_bitmap()
        self.m_panel9.Refresh()
        self.m_panel9.Update()

    def adjust_zoom( self, event=None):
        newzoom=float(self.m_textCtrl10.GetValue())
        self.m_panel9.set_zoom_level(newzoom)

    def zoom_in_10pct( self, event =None):
        currzoom=float(self.m_textCtrl10.GetValue())
        newzoom=currzoom-.1
        self.m_textCtrl10.SetValue(str(newzoom))
        self.adjust_zoom()

    def zoom_out_10pct( self, event=None ):
        currzoom = float(self.m_textCtrl10.GetValue())
        newzoom = currzoom + .1
        self.m_textCtrl10.SetValue(str(newzoom))
        self.adjust_zoom()

    def on_frame_iconize(self,event):
        self.parent.m_toolBar1.ToggleTool(self.parent.icnControlPanel.Id,False)
        # self.Iconize()

    def set_status(self,msg):
        self.m_statusBar1.SetStatusText(msg)

    def propogate_values( self, event=None ):
        # print "propogating values"
        # self.c.apm.tree_file=self.m_FilePicker_tree.GetPath()
        # self.c.apm.annotation_file=self.m_FilePicker_annotation.GetPath()
        pass

    def add_circles( self, event ):
        circs=self.m_spinCtrl2.GetValue()
        nd=self.parent.img_panel.aln.node_added_order[circs]
        print "Child Nodes:"
        if nd['cvs']<>None:
            for i in nd['cvs']:
                print " - %s, %s" % i
        print "This Node:"
        print " - %s, %s" % nd['vert']
        self.parent.img_panel.UpdateDrawing()


    def on_zoompanel_holder_paint(self,event):
        # print "zoompaint"
        self.m_panel9.Refresh()

    def redraw_tree(self,event=None):
        self.c.buffered_window.adjust_tree()

    def expand_clade_out(self,event=None):
        if self.c.buffered_window.active_edge is not None:
            w = float(self.m_textCtrl331.GetValue())
            w *= 1.05
            self.m_textCtrl331.SetValue(str(w))

    def expand_clade_in(self,event=None):
        if self.c.buffered_window.active_edge is not None:
            w = float(self.m_textCtrl331.GetValue())
            w /= 1.05
            self.m_textCtrl331.SetValue(str(w))

    def save_rp_file( self, event=None ):
        import pickle
        if os.path.exists(self.m_dirPicker4.GetPath()):
            f=open(os.path.join(self.m_dirPicker4.GetPath(),self.m_textCtrl17.GetValue()+'.rp'),'w')
            pickle.dump(self.c.buffered_window.radial_phylogram,f)
            f.close()




    def pivot_clock(self,event=None):
        if self.c.buffered_window.active_edge is not None:
            print "pivoting clockwise"
            t = float(self.m_textCtrl3311.GetValue())
            print "t: %s" % t
            t += 5.0/360.0*2.0*math.pi
            print "new t: %s" % t
            self.m_textCtrl3311.SetValue(str(t))

    def pivot_ctrclock(self,event=None):
        if self.c.buffered_window.active_edge is not None:
            t = float(self.m_textCtrl3311.GetValue())
            t -= 5.0/360.0*2.0*math.pi
            self.m_textCtrl3311.SetValue(str(t))

    def run_controller_script( self, event=None, text=None ):
        scripts.script_function(self.parent.img_panel)
        pass

    def run_controller_script_all(self, event=None):
        scripts.script_function_container()


    # def print_native_string( self, event=None ):
    #     f=self.m_fontPicker1.GetSelectedFont()
    #     # print f.GetNativeFontInfoDesc()
    #     # print ""
    #     # print f.GetNativeFontInfoUserDesc()

class alignment_gui_manager(gui_manager):
    def __init__(self,parent):
        gui_manager.__init__(self,parent)

    def change_starting_column(self, event):
        '''
        ALIGNMENT
        :param event:
        :return:
        '''
        v = self.m_startCol.GetValue()
        print "starting column changed to %s" % v
        self.parent.img_panel.ChangeStartingColumn(v)


    def save_alignment_image(self, event):
        tgt_file = os.path.join(self.m_dirPicker2.GetTextCtrlValue(),
                                self.m_textCtrl8.GetValue() + '_' + str(self.m_startCol.GetValue()) + '.jpg')
        self.parent.img_panel.SaveToFile(tgt_file, wx.BITMAP_TYPE_JPEG)

class abstract_image_manager(sfld_view.imgFrame):
    def __init__(self,parent):
        sfld_view.imgFrame.__init__(self,parent)

        # initialize controller and other misc
        self.c = controller.Controller()
        self.c.set_ImageFrame_referenece(self)
        self.sz=None

        # make control panel
        self.make_control_panel()

        # add window
        self.make_image_panel()

        # bind methods
        self.bind_methods()


    def make_control_panel(self):
        raise NotImplementedError

    def make_image_panel(self):
        raise NotImplementedError

    def bind_methods(self):
        raise NotImplementedError

    def set_status(self,msg):
        self.m_statusBar2.SetStatusText(msg)

class image_manager(abstract_image_manager):
    def __init__(self,parent):
        abstract_image_manager.__init__(self,parent)

    def make_control_panel(self):
        self.control_panel = gui_manager(self)
        self.control_panel.SetIcon(wx.Icon('resources/icnPhyloMain32.png'))
        self.control_panel.Show()
        self.control_panel.propogate_values()

    def right_dclick(self, event):
        print event.GetPosition()

    def bind_methods(self):
        self.img_panel.Bind(wx.EVT_RIGHT_DCLICK, self.right_dclick)

    def control_panel_tool_click(self,event=None):
        # print self.control_panel.IsActive()
        if self.control_panel.IsIconized()==True:
            self.control_panel.Iconize(False)
        self.control_panel.Raise()

    def make_image_panel(self):
        self.bSizer1 = wx.BoxSizer( wx.VERTICAL )
        # self.img_panel = view_classes.PhylogenyBufferedWindow(self)
        self.img_panel = view_classes.CairoPhylogenyBufferedWindow(self)
        self.img_panel.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        self.img_panel.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        self.bSizer1.Add( self.img_panel, 1, wx.EXPAND, 0 )
        self.SetSizer( self.bSizer1 )
        self.Layout()

class AlignmentImageManager(image_manager):
    def __init__(self,parent):
        image_manager.__init__(self,parent)

    def make_control_panel(self):
        self.control_panel = alignment_gui_manager(self)
        self.control_panel.SetIcon(wx.Icon('resources/icnPhyloMain32.png'))
        self.control_panel.Show()
        self.control_panel.propogate_values()

    def make_image_panel(self):
        self.bSizer1 = wx.BoxSizer( wx.VERTICAL )
        self.img_panel = view_classes.AlignmentBufferedWindow(self)
        self.img_panel.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        self.img_panel.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        self.bSizer1.Add( self.img_panel, 1, wx.EXPAND, 0 )
        self.SetSizer( self.bSizer1 )
        self.Layout()
