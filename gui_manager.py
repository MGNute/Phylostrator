__author__ = 'Michael'

from my_globals import *
import tree_manipulator as trman
import sfld_view
import view_classes
import controller
import wx
import os.path
import skimage.io
import skimage.transform
import skimage.draw
import numpy as np

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

        self.working_folder=None
        # self.cold_initialize()

        # self.initial_checks()
        # self.add_value_pickers()
        # self.populate_annotation_fields()

        self.c.circle_size=self.m_slider1.GetValue()

        #TODO: This is just for the verstion where we want to do a cold initialize, otherwise have to make the image frame
        #    decide whether to show itself, etc...

        # self.image_frame=image_manager(self)
        # self.c.set_ImageFrame_referenece(self.image_frame)
        # self.image_frame.Show()

    def cold_initialize(self):
        self.set_file()
        self.set_annotation_file()
        self.import_tree()
        self.import_annotation()

    def populate_annotation_fields(self):
        # ONLY EXECUTE THIS ONCE THE ANNOTATION HAS BEEN LOADED
        flds=self.c.annotation_fields
        self.m_ComboSelectedField.Clear()
        self.m_ComboSelectedField.AppendItems(flds)

        self.add_value_pickers()

        if 'subgroup_id' in flds:
            self.m_ComboSelectedField.SetValue('subgroup_id')
            self.populate_annotation_values()



    def populate_annotation_values(self,event=None):
        fld = self.m_ComboSelectedField.GetValue()
        self.c.apm.node_annotation_level=fld
        unqs = self.c.apm.node_annotation.uniques[fld]

        self.value_picker.set_values(unqs)
        self.m_panel5.Layout()
        self.value_picker.Fit(self.m_panel5)
        self.m_panel4.Layout()
        self.c.set_ValuePickerCtrl_reference(self.value_picker)

    def add_value_pickers(self):
        self.value_picker=view_classes.ValuePickerControl(self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER)

        self.m_panel5.SetSizer( self.value_picker)

        self.m_panel5.Layout()
        self.value_picker.Fit(self.m_panel5)
        self.m_panel4.Layout()
        self.Layout()

    def initial_checks(self):
        if self.m_FilePicker_tree.GetTextCtrlValue()<>'':
            self.set_file(filepath=self.m_FilePicker_tree.GetTextCtrlValue())
        if self.m_FilePicker_annotation.GetTextCtrlValue()<>'':
            self.annotation_file=self.m_FilePicker_annotation.GetTextCtrlValue()

    def set_file( self, event=None, filepath=None):
        fo=''
        self.c.apm.tree_file=self.m_FilePicker_tree.GetPath()
        # print self.c.tree_file
        try:
            fo, fi = os.path.split(self.c.apm.tree_file)
        except:
            pass
        self.working_folder=fo
        self.txt_workingFolder.SetValue(fo)

    def set_annotation_file( self, event=None, filepath=None):
        self.annotation_file=self.m_FilePicker_annotation.GetPath()

    def SaveCurrentImage(self,event):
        tgt_file=self.m_textImageSaveTarget.GetValue()
        tgt_path=os.path.join(self.working_folder,tgt_file)
        self.c.save_image(tgt_path)

    # def process_annotationvalue_check(self,event):
    #     checked=[]
    #     for i in self.value_picker.value_pickers:
    #         if i.m_checkBox1.IsChecked()==True:
    #             checked=(i.value, i.clr)
    #
    #     print checked

    def import_tree( self, event=None ):
        self.c.import_tree()

    def import_annotation( self, event=None ):
        self.c.import_annotation(self.annotation_file)

        if self.c.apm.state_tree_loaded==True:
            self.c.get_relevent_data_from_model()
            self.populate_annotation_fields()
        else:
            print "Tree not loaded, so no action taken."

    def trigger_redraw(self,event=None):
        self.c.circle_size=int(self.m_slider1.GetValue())
        self.c.trigger_refresh()

    def on_frame_close( self, event ):
        if event.CanVeto():
            event.Veto()
            self.Iconize()

    def on_frame_iconize(self,event):
        self.parent.m_toolBar1.ToggleTool(self.parent.icnControlPanel.Id,False)
        # self.Iconize()

    def set_status(self,msg):
        self.m_statusBar1.SetStatusText(msg)

    def propogate_values( self, event=None ):
        print "propogating values"
        self.c.apm.tree_file=self.m_FilePicker_tree.GetPath()
        self.c.apm.annotation_file=self.m_FilePicker_annotation.GetPath()

    def on_zoompanel_paint(self,event):
        print "zoompaint"
        self.m_panel6.Refresh()


#
#   Utility Function:
#
def convert_coordinates(xyrange,disprange,xycoords):
    '''
    Converts coordinates from the x-y plan based on the range "xyrange" (xmin, xmax, ymin, ymax) to the display coordinates

    :param xyrange: (xmin, xmax, ymin, ymax)
    :param disprange: (w , h) (indexed at 0, so max output will be (w-1, h-1)
    :param xycoords: (x,y)
    :return: display coords (on numpy scale) or None if it's out of the display range
    '''
    xnew = round((disprange[0]-1)*(xycoords[0]-xyrange[0])/(xyrange[1]-xyrange[0]), 0)
    ynew = disprange[1]-1 - round((disprange[1]-1)*(xycoords[1]-xyrange[2])/(xyrange[3]-xyrange[2]), 0)
    if xnew > disprange[0]-1 or xnew < 0 or ynew < 0 or ynew > disprange[1]-1:
        return None
    else:
        return (xnew,ynew)



class image_manager(sfld_view.imgFrame):

    def __init__(self,parent):
        sfld_view.imgFrame.__init__(self,parent)
        self.Bind(wx.EVT_PAINT,self.OnPaint)

        self.c=controller.Controller()

        self.view_range=self.c.max_data_dims
        self.current_bitmap=None

        self.eid_hash=None
        self.c.set_ImageFrame_referenece(self)

        self.control_panel=gui_manager(self)

        if self.icnControlPanel.IsToggled()==False:
            self.icnControlPanel.Toggle()
        self.m_toolBar1.Realize()


        self.control_panel.Show()
        self.control_panel.propogate_values()

    def save_dc_to_bitmap(self,tgt_path):
        self.current_bitmap.SaveFile(tgt_path,wx.BITMAP_TYPE_JPEG)

    def control_panel_tool_click(self,event=None):
        if self.control_panel.IsIconized()==True:
            self.control_panel.Iconize(False)
            print "IsIconized:\t " + str(self.control_panel.IsIconized())

        if event.IsChecked()==True:
            self.control_panel.Show()

        if event.IsChecked()==False:
            self.control_panel.Hide()

    def OnImgPaint(self,event):
        self.pdc=wx.PaintDC(self.img_panel)
        w=self.pdc.GetSize()[0]
        h=self.pdc.GetSize()[1]
        self.view_range=self.c.view_range

        if self.c.apm.state_tree_loaded:
            self.get_current_tree_image(w,h)

        if self.c.apm.state_node_annotation_loaded:
            self.draw_circles(w,h)

        if self.current_bitmap<>None:
            # print 'bitmap set to None'
            self.pdc.DrawBitmap(self.current_bitmap,0,0)

    def get_current_tree_image(self,w,h):
        self.current_bitmap=wx.EmptyBitmap(w,h)
        self.memdc=wx.MemoryDC(self.current_bitmap)
        self.memdc.Clear()

        sz=(w,h)


        for i in self.c.apm.segments:
            x1=convert_coordinates(self.view_range,sz,i[0])
            x2=convert_coordinates(self.view_range,sz,i[1])
            if x1 is not None and x2 is not None:
                self.memdc.DrawLine(x1[0],x1[1],x2[0],x2[1])

        self.memdc.SelectObject(wx.NullBitmap)

    def draw_circles(self,w,h,header_field=None,value=None):

        sz=(w,h)
        circ_size=self.c.circle_size
        list_of_circles=self.c.get_circle_sets_by_color()

        self.memdc.SelectObject(self.current_bitmap)
        curr_brush=self.memdc.GetBrush()
        for i in list_of_circles:
            self.memdc.SetBrush(wx.Brush(wx.Colour(i[0],i[1],i[2]),wx.SOLID))
            for j in list_of_circles[i]:
                x=convert_coordinates(self.view_range,sz,j)
                self.memdc.DrawCirclePoint(wx.Point(x[0],x[1]),circ_size)

        self.memdc.SetBrush(curr_brush)
        self.memdc.SelectObject(wx.NullBitmap)

    def set_status(self,msg):
        self.m_statusBar2.SetStatusText(msg)
        self.control_panel.set_status(msg)



