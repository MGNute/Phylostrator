__author__ = 'Michael'
import wx
import wx.lib.scrolledpanel
import pickle
import dendropy
import controller
import aux_view_classes as avc
from view import *
import my_globals, alignment
import numpy as np
global colors
import tree_manipulator as tm
from utilities import *
from sfld_view import AddTxtDialog

class ValuePickerControl(wx.BoxSizer):
    def __init__(self,parent,*args):
        wx.BoxSizer.__init__(self,wx.VERTICAL)
        # self.panel=wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
        # self.panel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ))
        # self.panel.SetBackgroundColour( wx.Colour( 255, 234, 213 ))
        #
        # self.m_staticText8 = wx.StaticText( parent, wx.ID_ANY, u"Values", wx.DefaultPosition, wx.DefaultSize, 0 )
        # self.m_staticText8.Wrap( -1 )
        # self.m_staticText8.SetFont( wx.Font( 11, 72, 90, 92, False, "Cambria" ) )
        # self.Add(self.m_staticText8,0, wx.ALL,5)
        #
        # self.szr_ValuesVert = wx.BoxSizer( wx.VERTICAL )
        self.parent=parent
        self.value_pickers=[]
        self.values=None
        self.colors=None

        # self.set_values(['189'])

    def clear_all(self):
        self.Clear(True)
        self.values=[]
        self.value_pickers=[]

    def set_values(self,vals=None):
        self.clear_all()
        if vals != None:
            self.values=vals

        k=0

        self.colors={}
        for i in self.values:
            if k>=len(colors):
                clr=get_random_color()
            else:
                clr=colors[k]
                k+=1
            self.colors[i]=clr


            # a=self.ValuePicker(self.parent,i,clr,val_ctrl=self)
            a = ValuePicker(self.parent, i, clr, val_ctrl=self)
            self.Add(a,0, wx.EXPAND, 5)
            self.value_pickers.append(a)

        self.add_final_spacer()

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
            vp = ValuePicker(**i)
            self.Add(vp,0, wx.EXPAND,5)
            self.value_pickers.append(vp)
        self.add_final_spacer()
        self.Layout()

class ValuePicker(wx.BoxSizer):
    c=None
    def __init__(self,parent=None, value=None,clr=None, sz=3, checked=False, val_ctrl=None):
        if self.c is None:
            self.c=controller.Controller()
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
        self.m_checkBox1.Bind(wx.EVT_LEFT_DCLICK,self.move_down_in_list)

    def move_down_in_list(self,event):
        fld=self.c.apm.node_annotation_level
        ind=self.c.apm.node_annotation.uniques[fld].index(self.value)
        # print self.c.apm.node_annotation.uniques[fld]
        self.c.apm.node_annotation.uniques[fld].pop(ind)
        self.c.apm.node_annotation.uniques[fld].append(self.value)
        # self.c.trigger_annotation_picker_refresh()

        self.value_picker_control.move_to_bottom(self.value)


    def process_annotationvalue_check(self,event=None):
        self.c.update_circles_by_annotation()
        self.c.trigger_refresh()

    def process_color_change(self,event):
        newcolor=self.m_colourPicker1.GetColour()
        self.clr=newcolor.Get()
        self.c.update_circles_by_annotation()
        self.c.trigger_refresh()

    def process_size_change(self,event):
        print "processing size change"
        self.size=int(self.m_spinCtrl.GetValue())
        self.c.update_circles_by_annotation()
        self.c.trigger_refresh()


class SEPPValuePickerControl(ValuePickerControl):
    def __init__(self, parent, *args):
        ValuePickerControl.__init__(self,parent, *args)


    def set_values(self, vals=None):
        self.clear_all()
        if vals != None:
            self.values = vals

        k = 0

        self.colors = {}
        for i in self.values:
            if k >= len(colors):
                clr = get_random_color()
            else:
                clr = colors[k]
                k += 1
            self.colors[i] = clr

            # a=self.ValuePicker(self.parent,i,clr,val_ctrl=self)
            a = SEPPValuePicker(self.parent, i, clr, val_ctrl=self)
            self.Add(a, 0, wx.EXPAND, 5)
            self.value_pickers.append(a)

        self.add_final_spacer()


    def load_values(self, val_temps):
        self.clear_all()
        for i in val_temps:
            # vp=self.ValuePicker(**i)
            vp = SEPPValuePicker(**i)
            self.Add(vp, 0, wx.EXPAND, 5)
            self.value_pickers.append(vp)
        self.add_final_spacer()
        self.Layout()

class SEPPValuePicker(wx.BoxSizer):
    '''
    Tons of code duplcation here but not sure what else to do about that.
    '''
    def __init__(self, parent=None, value=None, clr=None, sz=2, checked=False, val_ctrl=None):
        self.c = controller.SEPPController()
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
        self.m_checkBox1.Bind(wx.EVT_LEFT_DCLICK,self.move_down_in_list)

    def move_down_in_list(self,event):
        pass

    def process_annotationvalue_check(self,event=None):
        self.c.update_circles_by_annotation()
        self.c.trigger_refresh()

    def process_color_change(self,event):
        newcolor=self.m_colourPicker1.GetColour()
        self.clr=newcolor.Get()
        self.c.update_circles_by_annotation()
        self.c.trigger_refresh()

    def process_size_change(self,event):
        print "processing size change"
        self.size=int(self.m_spinCtrl.GetValue())
        self.c.update_circles_by_annotation()
        self.c.trigger_refresh()







USE_BUFFERED_DC = True

# class BufferedWindow(wx.Window):
class BufferedWindow(wx.Panel):
    """

    A Buffered window class.

    To use it, subclass it and define a Draw(DC) method that takes a DC
    to draw to. In that method, put the code needed to draw the picture
    you want. The window will automatically be double buffered, and the
    screen will be automatically updated when a Paint event is received.

    When the drawing needs to change, you app needs to call the
    UpdateDrawing() method. Since the drawing is stored in a bitmap, you
    can also save the drawing to file by calling the
    SaveToFile(self, file_name, file_type) method.

    """
    def __init__(self, *args, **kwargs):
        # make sure the NO_FULL_REPAINT_ON_RESIZE style flag is set.
        kwargs['style'] = kwargs.setdefault('style', wx.NO_FULL_REPAINT_ON_RESIZE) | wx.NO_FULL_REPAINT_ON_RESIZE
        wx.Window.__init__(self, *args, **kwargs)

        wx.EVT_PAINT(self, self.OnPaint)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_RIGHT_DCLICK(self,self.OnRightDclick)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)
        self.paint_count = 0

    def Draw(self,dc):
        ## just here as a place holder.
        ## This method should be over-ridden when subclassed
        pass

    def OnRightDclick(self, event):
        print event.GetPosition()

    def OnPaint(self, event):
        self.paint_count += 1
        # print "OnPaint called: ", self.paint_count
        # All that is needed here is to draw the buffer to screen

        if USE_BUFFERED_DC:
            dc = wx.BufferedPaintDC(self, self._Buffer)
        else:
            dc = wx.PaintDC(self)
            memdc = wx.MemoryDC()
            memdc.SelectObject(self._Buffer)
            dc.Blit(0, 0, self._Buffer.Width, self._Buffer.Height, memdc, 0, 0)
            # dc.DrawBitmap(self._Buffer, 0, 0)

    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size  = self.GetClientSizeTuple()


        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.EmptyBitmap(*Size)
        self.UpdateDrawing()

    def SaveToFile(self,FileName,FileType=wx.BITMAP_TYPE_JPEG):
        ## This will save the contents of the buffer
        ## to the specified file. See the wxWindows docs for
        ## wx.Bitmap::SaveFile for the details
        self._Buffer.SaveFile(FileName,FileType)

    def UpdateDrawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. If that data changes, the drawing needs to
        be updated.

        This code re-draws the buffer, then calls Update, which forces a paint event.
        """
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)
        self.Draw(dc)
        self.Refresh()
        self.Update()

class PhylogenyBufferedWindow(BufferedWindow):
    def __init__(self,parent,*args, **kwargs):
        self.parent=parent
        self.circles=None
        self.c = controller.Controller()
        self.c.set_BufferedWindow_reference(self)
        self.tree_path = my_globals.amato_qiime_tree
        self.radial_phylogram = tm.Radial_Phylogram(self.tree_path)
        # self.c.apm.state_tree_loaded=True
        self.set_initial_corners()
        self.zoom=1.0
        self.rotation=0.0
        self.DrawData={}
        self.ExtraDrawCircles=[]
        self.ExtraDrawSegments=[]
        self.SeppDrawCircles=None
        self.LegendDrawData=None


        self.MakeDrawData()
        BufferedWindow.__init__(self,parent, *args, **kwargs)
        self.set_corner_boundaries()
        self.c.zoom_panel.phylogeny_viewer_loaded()

        self.Bind(wx.EVT_LEFT_DOWN, self.on_click)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_double_click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click)

    def on_click( self, event ):
        # print "mouse_clicked"
        # self.parent.m_statusBar2.SetStatusText("Panel Space -- x: %s, y: %s" % event.GetPositionTuple(),1)
        self.parent.m_statusBar2.SetStatusText("Tree Space -- x: %s, y: %s" % self.transform_coordinate(event.GetPositionTuple(),True), 1)

        tscoord = self.transform_coordinate(event.GetPositionTuple(), True)
        # print event.GetPositionTuple()
        # print tscoord
        # print self.transform_coordinate(tscoord,False)
        minlen = 99999999.0
        eref = None
        ct = 0
        for i in self.radial_phylogram.myt.preorder_edge_iter():
            if i.viewer_edge is not None:
                # ct +=1
                ln = distance_to_line_segment(i.viewer_edge.head_x, i.viewer_edge.tail_x, tscoord)
                # ln = distance_to_line_segment(i.head_node.viewer_node.ts_x, i.tail_node.viewer_node.ts_x, tscoord)
                if ln < minlen:
                    ct +=1
                    # print "ln
                    minlen = ln
                    eref = (i,ln)
        # print "checked %s edges" % ct

        pos1 = "(%.2f, %.2f)" % eref[0].head_node.viewer_node.ts_x
        pos2 = "(%.2f, %.2f)" % eref[0].tail_node.viewer_node.ts_x
        # self.parent.m_statusBar2.SetStatusText("head: %s, %s |tail: %s, %s| len: %s" % (eref[0].head_node.label,eref[0].head_node.viewer_node.ts_x,eref[0].tail_node.label,
        #                                                                                   eref[0].tail_node.viewer_node.ts_x, eref[1]),2)
        self.parent.m_statusBar2.SetStatusText("head: %s, %s |tail: %s, %s| len: %s" % (eref[0].head_node.label, pos1, eref[0].tail_node.label,
                                                                                          pos2, eref[1]),2)


        # self.parent.m_statusBar2.SetStatusText("head: %s, %s |tail: %s, %s| len: %s" % (eref[0].head_node.label,eref[0].viewer_edge.head_x,eref[0].tail_node.label,
        #                                                                                   eref[0].viewer_edge.tail_x, eref[1]),2)
        # self.parent.m_statusBar2.SetStatusText("head_x: %s\ttail_x: %s\tlen: %s" % (eref[0].viewer_edge.head_x, eref[0].viewer_edge.tail_x, eref[1]),0 )
        self.AddToExtraDrawSegments((eref[0].viewer_edge.head_x, eref[0].viewer_edge.tail_x))
        self.UpdateDrawing()


    def on_double_click(self,event):
        tscoord = self.transform_coordinate(event.GetPositionTuple(), True)
        # print event.GetPositionTuple()
        # print tscoord
        # print self.transform_coordinate(tscoord,False)
        minlen = 99999999.0
        eref = None
        ct = 0
        for i in self.radial_phylogram.myt.preorder_edge_iter():
            if i.viewer_edge is not None:
                # ct +=1
                ln = distance_to_line_segment(i.viewer_edge.head_x, i.viewer_edge.tail_x, tscoord)
                # ln = distance_to_line_segment(i.head_node.viewer_node.ts_x, i.tail_node.viewer_node.ts_x, tscoord)
                if ln < minlen:
                    ct +=1
                    # print "ln
                    minlen = ln
                    eref = (i,ln)
        newtree = eref[0].head_node.extract_subtree()
        newtree_tree = dendropy.Tree(seed_node = newtree)
        newtree_tree.write(path=my_globals.amato_temp_subtree,schema = "newick")
        print "wrote the tree from node %s and below to the subtree path" % eref[0].tail_node.label


    def on_right_click( self, event ):
        print "mouse_clicked"
        self.ClearExtraDrawSegments()
        self.UpdateDrawing()
        # self.parent.m_statusBar2.SetStatusText("x: %s, y: %s" % event.GetPositionTuple(),1)

    def import_new_tree(self,treepath):
        del self.radial_phylogram
        self.tree_path=treepath
        self.radial_phylogram=tm.Radial_Phylogram(self.tree_path)
        self.c.circle_sets_by_color = None
        self.set_initial_corners()
        self.zoom=1.0
        self.rotation=0.0
        self.DrawData={}
        self.MakeDrawData()
        self.set_corner_boundaries()
        self.c.zoom_panel.phylogeny_viewer_loaded()


    def set_initial_corners(self):
        max_dims=self.radial_phylogram.get_max_dims()
        print "max dims: %s, %s, %s, %s" % max_dims
        self.top_left=(max_dims[0],max_dims[3])
        self.bottom_right=(max_dims[1],max_dims[2])

    def ClearExtraDrawData(self):
        del self.ExtraDrawCircles
        self.ExtraDrawCircles = []

    def ClearExtraDrawSegments(self):
        del self.ExtraDrawSegments
        self.ExtraDrawSegments = []

    def AddToExtraDrawCircles(self,i):
        # should be ((x,y),r,g,b,width)
        self.ExtraDrawCircles.append(i)

    def AddToExtraDrawSegments(self,i):
        self.ExtraDrawSegments.append(i)




    def MakeDrawData(self):

        self.DrawData['segments']=[]

        for i in self.radial_phylogram.segments:
            self.DrawData['segments'].append((i[0][0],i[0][1],i[1][0],i[1][1]))
        max_dims=self.radial_phylogram.get_max_dims()
        self.top_left=(max_dims[0],max_dims[3])
        self.bottom_right=(max_dims[1],max_dims[2])


    def UpdateMiscInfoOnDraw(self):
        self.c.image_frame.control_panel.m_textHeight.SetValue(str(self._Buffer.Height))
        self.c.image_frame.control_panel.m_textWidth.SetValue(str(self._Buffer.Width))

    def Draw(self,dc):
        dc.SetBackground(wx.Brush("White"))
        dc.Clear()
        dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
        self.h=self._Buffer.Height
        self.w=self._Buffer.Width
        xyrange=(self.top_left[0],self.bottom_right[0],self.bottom_right[1],self.top_left[1])
        self.c.bw_aspect_ratio=float(self.w)/float(self.h)
        self.line_list = []
        self.set_coordinate_transform()
        for i in self.DrawData['segments']:
            # x1 = convert_coordinates(xyrange,(self.w,self.h),(i[0],i[1]))
            # x2 = convert_coordinates(xyrange, (self.w, self.h), (i[2], i[3]))
            # self.line_list.append((x1[0],x1[1],x2[0],x2[1]))
            seg=self.get_segment_for_rendering((i[0],i[1]),(i[2],i[3]))
            if seg <> None:
                self.line_list.append(seg)

        dc.DrawLineList(self.line_list)
        if self.c.circle_sets_by_color<>None:
            self.DrawCircles(dc)

        if len(self.ExtraDrawCircles)>0:
            self.DrawExtraCircles(dc)

        if self.SeppDrawCircles is not None:
            self.DrawExtraCircles(dc,self.SeppDrawCircles)

        if len(self.ExtraDrawSegments)>0:
            self.DrawExtraSegments(dc)

        if self.LegendDrawData<>None:
            self.DrawLegend(dc)

        if self.c.zoom_panel.viewer_loaded==True:
            self.c.zoom_panel.set_box_coords()
            self.c.zoom_panel.Update()

    def DrawLegend(self,dc):
        curr_brush = dc.GetBrush()
        # print self.LegendDrawData['entries']
        # print self.LegendDrawData['entries'][0][1]
        textent = dc.GetTextExtent(self.LegendDrawData['entries'][0][0])
        h = self.LegendDrawData['H']
        w = self.LegendDrawData['W']
        gap = textent[1]
        for i in self.LegendDrawData['entries']:
            dc.SetBrush(wx.Brush(i[1]))
            dc.DrawRectangle(w,h,gap,gap)
            dc.DrawText(i[0],w+gap+2,h)
            h+=(gap+2)
        dc.SetBrush(curr_brush)



    def DrawCircles(self,dc):
        # print "Drawing Circles"
        curr_brush = dc.GetBrush()
        for i in self.c.circle_sets_by_color:
            dc.SetBrush(wx.Brush(wx.Colour(i[0],i[1],i[2]),wx.SOLID))
            for j in self.c.circle_sets_by_color[i]:
                x=self.transform_coordinate(j[0])
                # print x
                dc.DrawCirclePoint(wx.Point(x[0],-x[1]),j[1])
        dc.SetBrush(curr_brush)

    def DrawExtraSegments(self,dc):
        curr_pen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.RED,.5))
        for i in self.ExtraDrawSegments:
            x1 = self.transform_coordinate(i[0])
            x2 = self.transform_coordinate(i[1])
            dc.DrawLine(x1[0],-x1[1],x2[0],-x2[1])
            # print "drawing red line from (%s, %s) to (%s, %s)" % (x1[0],x1[1],x2[0],x2[1])
        dc.SetPen(curr_pen)

    def DrawExtraCircles(self,dc,circle_set=None):
        curr_brush = dc.GetBrush()
        curr_pen = dc.GetPen()
        if circle_set is None:
            circle_set = self.ExtraDrawCircles
        for i in circle_set:
            x=self.transform_coordinate(i[0])
            dc.SetBrush(wx.Brush(wx.Colour(i[1],i[2],i[3]),wx.SOLID))
            if len(i)>5 and i[5] is not None:
                dc.SetPen(i[5])

            dc.DrawCirclePoint(wx.Point(x[0],-x[1]),i[4])
        dc.SetBrush(curr_brush)
        dc.SetPen(curr_pen)

    def transform_coordinate(self,x1,inverse=False):
        '''
        inverse is True when we are going from panel coordinates to tree-space coordinates. False otherwise
        '''
        if inverse==False:
            return (self.t11 * x1[0] + self.t12 * x1[1] + self.t13, self.t21 * x1[0] + self.t22 * x1[1] + self.t23)
        else:
            return (self.t11_inv * x1[0] + self.t12_inv * x1[1] + self.t13_inv, self.t21_inv * x1[0] + self.t22_inv * x1[1] + self.t23_inv)

    def get_segment_for_rendering(self,x1,x2):
        # first transform coordinates
        x1n=(self.t11*x1[0]+self.t12*x1[1]+self.t13,self.t21*x1[0]+self.t22*x1[1]+self.t23)
        x2n = (self.t11 * x2[0] + self.t12 * x2[1] + self.t13, self.t21 * x2[0] + self.t22 * x2[1] + self.t23)
        #NOTE: Y coordinates are still negative at this point and need a sign change before rendering
        # newpts=get_line_on_screen(x1n,x2n,self.h,self.w)
        newpts = (x1n,x2n)
        if newpts==None:
            return None
        else:
            #finally, convert the y values to positive for rendering
            return (round(newpts[0][0],0),round(-newpts[0][1],0),round(newpts[1][0],0),round(-newpts[1][1],0))

    def set_coordinate_transform(self):
        w=self.w
        h=self.h
        max_dims = (self.top_left[0], self.bottom_right[0], self.bottom_right[1], self.top_left[1])
        aspect = abs((max_dims[1] - max_dims[0]) / (max_dims[3] - max_dims[2]))
        if aspect > (w / h):
            # constraining dimension is horizontal
            vgap = (h - w / aspect) / 2
            hgap = 0
        else:
            # constraining dimension is horizontal
            vgap = 0
            hgap = (w - h * aspect) / 2

        a = np.array(([max_dims[0], max_dims[2], 1], [max_dims[0], max_dims[3], 1], [max_dims[1], max_dims[3], 1]),
                     dtype=np.float64)
        ainv = np.linalg.inv(a)
        tx = np.dot(ainv, np.array([hgap, hgap, w - 1 - hgap], dtype=np.float64))
        ty = np.dot(ainv, np.array([vgap - (h - 1), -vgap, -vgap], dtype=np.float64))
        theta = float(self.rotation)/360.0 * 2 * math.pi
        rotmat = np.array(([math.cos(theta),-math.sin(theta),0],[math.sin(theta),math.cos(theta),0],[0,0,1]),dtype=np.float64)
        final_trans=np.dot(np.vstack((tx,ty)),rotmat)
        self.t11 = np.asscalar(final_trans[0,0])
        self.t12 = np.asscalar(final_trans[0,1])
        self.t13 = np.asscalar(final_trans[0,2])
        self.t21 = np.asscalar(final_trans[1,0])
        self.t22 = np.asscalar(final_trans[1,1])
        self.t23 = np.asscalar(final_trans[1,2])
        self.set_inverse_transform()


    def set_inverse_transform(self):
        '''
        sets the values to go from panel coordinates to tree-space coordinates
        '''
        a=np.array(([self.t11,self.t12,self.t13],[-self.t21,-self.t22,-self.t23],[0,0,1]),dtype=np.float64)
        b=np.linalg.inv(a)
        self.t11_inv = np.asscalar(b[0, 0])
        self.t12_inv = np.asscalar(b[0, 1])
        self.t13_inv = np.asscalar(b[0, 2])
        self.t21_inv = np.asscalar(b[1, 0])
        self.t22_inv = np.asscalar(b[1, 1])
        self.t23_inv = np.asscalar(b[1, 2])


    def set_corner_boundaries(self,initial=True,topleft=None,bottomright=None):

        if topleft<>None:
            self.top_left=topleft
        if bottomright<>None:
            self.bottom_right=bottomright

        if initial==True:
            max_dims=self.radial_phylogram.get_max_dims()
            self.top_left=(max_dims[0],max_dims[3])
            self.bottom_right=(max_dims[1],max_dims[2])
        else:
            max_dims=(self.top_left[0],self.bottom_right[0],self.bottom_right[1],self.top_left[1])

    def get_global_boundingbox_image(self):
        self.global_bounding_box=(0,0,0,0)
        self.global_image_dc = wx.MemoryDC(wx.NullBitmap)
        self.global_image = wx.EmptyBitmap()


    def set_rotation(self,rotation=0.0):
        # self.radial_phylogram.set_rotation(rotation)
        self.rotation=rotation
        # print "old coordinate transforms: %s, %s, %s; %s, %s, %s" % (self.t11, self.t12, self.t13,self.t21, self.t22, self.t23)
        self.set_coordinate_transform()
        # print "new coordinate transforms: %s, %s, %s; %s, %s, %s" % (self.t11, self.t12, self.t13, self.t21, self.t22, self.t23)
        # self.MakeDrawData()
        self.UpdateDrawing()
        print "done redrawing"



class HOCRbufferedWindow(BufferedWindow):
    def __init__(self,parent,*args, **kwargs):
        # self.DrawData=self.MakeNewData()
        # BufferedWindow.__init__(self,parent,*args,**kwargs)


        self.DrawData={'ticks': my_globals.ticks, 'racers':my_globals.racers }
        # self.DrawData=self.MakeNewData()
        # print args
        # print kwargs
        BufferedWindow.__init__(self,parent, *args, **kwargs)

    def convert_time_to_window(self,time_coords,tc2=None):
        '''
        :param time_coords: comes in the form (time, position on racecourse)
        :return:
        '''
        topleft=(50,100)
        h=400
        w=1800
        mintime=my_globals.ticks[0][1]
        numticks=len(my_globals.ticks)
        maxtime=my_globals.ticks[numticks-1][1]

        y=int((1-time_coords[1])*h+topleft[1])
        x=int(topleft[0] + w*(time_coords[0]-mintime)/(maxtime-mintime))
        if tc2==None:
            return (x,y)
        else:
            y2=int((1-tc2[1])*h+topleft[1])
            x2=int(topleft[0] + w*(time_coords[0]-mintime)/(maxtime-mintime))
            return(x,y,x2,y2)


    def Draw(self,dc):
        dc.SetBackground(wx.Brush("White"))
        dc.Clear()


        dc.DrawLine(50,100,1850,100)
        dc.DrawLine(50,500,1850,500)
        for i in self.DrawData['ticks']:
            lab=i[0]
            t=i[1]
            x,y=self.convert_time_to_window((t,0))
            dc.DrawLine(x,y,x,y+10)
            tw,th=dc.GetTextExtent(lab)
            dc.DrawRotatedText(lab,x+int(th/2),y+10,270)

        for i in self.DrawData['racers']:
            x1,y1=self.convert_time_to_window((i[0],0))
            x2,y2=self.convert_time_to_window((i[1],1))
            dc.DrawLine(x1,y1,x2,y2)

class AlignmentBufferedWindow(BufferedWindow):
    def __init__(self,parent,*args, **kwargs):
        self.parent=parent
        # self.aln=alignment.MultipleSequenceAlignment()
        self.aln=pickle.load(open(my_globals.test_root + '\\alignment.pkl','rb'))
        # self.save_alignment(self.aln,my_globals.test_root + '\\alignment.pkl')
        self.c = controller.AlignmentController()

        # self.aln_bp=alignment.MultipleSequenceAlignment()
        # self.save_alignment(self.aln_bp,my_globals.test_root + '\\alignment_bp.pkl')


        self.MakeDrawData()
        BufferedWindow.__init__(self,parent, *args, **kwargs)

    def save_alignment(self,alnmt,filename):
        pickle.dump(alnmt,open(filename,'wb'))

    # def convert_time_to_window(self,time_coords,tc2=None):
    #     '''
    #     :param time_coords: comes in the form (time, position on racecourse)
    #     :return:
    #     '''
    #     topleft=(50,100)
    #     h=400
    #     w=1800
    #     mintime=my_globals.ticks[0][1]
    #     numticks=len(my_globals.ticks)
    #     maxtime=my_globals.ticks[numticks-1][1]
    #
    #     y=int((1-time_coords[1])*h+topleft[1])
    #     x=int(topleft[0] + w*(time_coords[0]-mintime)/(maxtime-mintime))
    #     if tc2==None:
    #         return (x,y)
    #     else:
    #         y2=int((1-tc2[1])*h+topleft[1])
    #         x2=int(topleft[0] + w*(time_coords[0]-mintime)/(maxtime-mintime))
    #         return(x,y,x2,y2)

    def UpdateMiscInfoOnDraw(self):
        self.c.image_frame.control_panel.m_textHeight.SetValue(str(self._Buffer.Height))
        self.c.image_frame.control_panel.m_textWidth.SetValue(str(self._Buffer.Width))

    def ChangeStartingColumn(self,value):
        self.DrawData['starting_col']=value
        col=self.aln.msa_cols[value]
        # print len(col.chars)
        # print col.chars
        self.UpdateDrawing()

    def MakeDrawData(self):
        # self.aln.get_cladogram_segments()
        self.DrawData={'starting_col': self.parent.control_panel.m_startCol.GetValue(), 'aln': self.aln }
        self.DrawData['tree_segs']=self.aln.segment_endpoints

    def Draw(self,dc):
        self.UpdateMiscInfoOnDraw()
        dc.SetBackground(wx.Brush("White"))
        dc.Clear()
        dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
        dc.DrawLineList(self.aln.segment_endpoints)
        w=8
        h=6
        topleft=(50,50)
        numcols=150


        self.DrawCharacterBoxesAtPosition(dc,self.DrawData['starting_col'],w,h,topleft,numcols)

    def DrawFNGrid(self,dc):
        self.UpdateMiscInfoOnDraw()
        dc.SetBackground(wx.Brush("White"))
        dc.Clear()


        w=6
        topleft=(50,50)
        dc.DrawRectangle(topleft[0],topleft[1],1+100*w,1+100*w)
        tp=self.DrawData['aln'].msa_cols[self.DrawData['starting_col']].tp_mat
        fn=self.DrawData['aln'].msa_cols[self.DrawData['starting_col']].fn_mat
        true_est_pos=np.where(tp-fn >0)
        fn_est=np.where(fn>0)
        print "tp: %s" % str(np.sum(tp)/2)
        print "fn: %s" % str(np.sum(fn)/2)
        # dc.SetPen(wx.Pen(wx.Colour(100,100,100),width=w+2))
        recs=[]
        for i in range(true_est_pos[0].shape[0]):
            x=true_est_pos[0][i]
            y=true_est_pos[1][i]
            recs.append((x*w+topleft[0]+1,y*w+topleft[0]+1,w,w))
        dc.DrawRectangleList(recs,pens=wx.TRANSPARENT_PEN,brushes=wx.Brush(wx.Colour(50,50,50)))

        # dc.SetPen(wx.Pen(wx.Colour(255,0,0),width=w+2))
        recs=[]
        for i in range(fn_est[0].shape[0]):
            x=fn_est[0][i]
            y=fn_est[1][i]
            recs.append((x*w+topleft[0]+1,y*w+topleft[0]+1,w,w))
        dc.DrawRectangleList(recs,pens=wx.TRANSPARENT_PEN,brushes=wx.Brush(wx.Colour(255,0,0)))

        # dc.DrawLineList(self.DrawData['tree_segs'])
        dc.SetPen(wx.Pen(wx.Colour(0,0,0)))
        dc.DrawLineList(self.aln.segment_endpoints)
        self.DrawCharacterBoxes(dc,w,topleft)


        # print "drew_lines"
        # b=dc.GetBrush()
        # p=dc.GetPen()
        # dc.SetBrush(wx.Brush(wx.Colour(255,0,0)))
        # dc.SetPen(wx.TRANSPARENT_PEN)
        # circs=self.c.image_frame.control_panel.m_spinCtrl2.GetValue()
        # for i in self.aln.node_added_order[0:(circs+1)]:
        #     # if self.c.image_frame.control_panel.m_chkAddSlow.IsChecked()==True:
        #         # time.sleep(0.33)
        #     a=self.aln.tree_vertices[i['nd']]
        #     dc.DrawCircle(a[0],a[1],3)
        # dc.SetPen(p)
        # dc.SetBrush(b)
        # dc.DrawPointList(self.aln.tree_vertices.values(),wx.Pen(wx.Colour(0,0,255),width=3))

    def DrawAnnotation(self,dc):
        dc.SetFont(wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Cambria" ))
        dc.DrawText("Gutell 16S.B.ALL - R0 - subset size 100",25,25)
        dc.DrawText("<-- Taxon (arranged by phylogeny) -->")

    def DrawCharacterBoxes(self,dc,w,h,topleft):
        d=dc.GetBrush()
        p=dc.GetPen()
        dc.SetPen(wx.TRANSPARENT_PEN)
        left_boundary=topleft[0]+w*100+3
        # top_bound=topleft[1]
        col=self.aln.msa_cols[self.DrawData['starting_col']]
        # ('A',Orange); ('C',Blue); ('G':Yellow): ('T':Green)}
        myclrs=[wx.Colour(255,153,0),wx.Colour(0,0,255),wx.Colour(255,255,0),wx.Colour(0,255,0),wx.Colour(50,50,50),wx.Colour(150,150,150)]
        for j in col.chars.keys():
            top_bound=topleft[1]+1+j*w
            site=col.chars[j][0]-1
            if site >= 0:
                dc.SetBrush(wx.Brush(myclrs[site]))
                dc.DrawRectangle(left_boundary,top_bound,w,h)
        dc.SetBrush(d)
        dc.SetPen(p)

    def DrawCharacterBoxesAtPosition(self,dc,colnum,w,h,topleft,numcols):
        d=dc.GetBrush()
        p=dc.GetPen()
        dc.SetPen(wx.TRANSPARENT_PEN)
        left_boundary=topleft[0]
        # top_bound=topleft[1]
        # print "starting at %s, spanning %s cols" % (colnum, numcols)

        for i in range(numcols):
            col=self.aln.msa_cols[colnum+i]
            # ('A',Orange); ('C',Blue); ('G':Yellow): ('T':Green)}
            myclrs=[wx.Colour(255,153,0),wx.Colour(0,0,255),wx.Colour(255,255,0),wx.Colour(0,255,0),wx.Colour(50,50,50),wx.Colour(125,76,126),wx.Colour(125,255,0)]
            for j in col.chars.keys():
                top_bound=topleft[1]+1+j*h
                site=col.chars[j][0]-1
                if site >= 0:
                    try:
                        dc.SetBrush(wx.Brush(myclrs[site]))
                    except:
                        print (site,j,colnum,i,col.node_order_lookup.keys()[col.node_order_lookup.values().index(j)])
                        # print colnum+i
                    dc.DrawRectangle(left_boundary,top_bound,w,h)
            left_boundary+=w

        dc.SetBrush(d)
        dc.SetPen(p)
        dc.DrawText(str(colnum),topleft[0],topleft[1]-15)
        dc.DrawText(str(colnum+50),650,topleft[1]-15)
        dc.DrawText(str(colnum+100),1250,topleft[1]-15)

        # dc.DrawLine(50,100,1850,100)
        # dc.DrawLine(50,500,1850,500)
        # for i in self.DrawData['ticks']:
        #     lab=i[0]
        #     t=i[1]
        #     x,y=self.convert_time_to_window((t,0))
        #     dc.DrawLine(x,y,x,y+10)
        #     tw,th=dc.GetTextExtent(lab)
        #     dc.DrawRotatedText(lab,x+int(th/2),y+10,270)
        #
        # for i in self.DrawData['racers']:
        #     x1,y1=self.convert_time_to_window((i[0],0))
        #     x2,y2=self.convert_time_to_window((i[1],1))
        #     dc.DrawLine(x1,y1,x2,y2)


    # def right_dclick(self,event=None):
    #     print "here"
    #     print event.GetPosition()

    # def Draw(self, dc):
    #     dc.SetBackground( wx.Brush("White") )
    #     dc.Clear() # make sure you clear the bitmap!
    #
    #     # Here's the actual drawing code.
    #     for key,data in self.DrawData.items():
    #         if key == "Rectangles":
    #             dc.SetBrush(wx.BLUE_BRUSH)
    #             dc.SetPen(wx.Pen('VIOLET', 4))
    #             for r in data:
    #                 dc.DrawRectangle(*r)
    #         elif key == "Ellipses":
    #             dc.SetBrush(wx.Brush("GREEN YELLOW"))
    #             dc.SetPen(wx.Pen('CADET BLUE', 2))
    #             for r in data:
    #                 dc.DrawEllipse(*r)
    #         elif key == "Polygons":
    #             dc.SetBrush(wx.Brush("SALMON"))
    #             dc.SetPen(wx.Pen('VIOLET RED', 4))
    #             for r in data:
    #                 dc.DrawPolygon(r)
    #
    #
    # def MakeNewData(self):
    #     ## This method makes some random data to draw things with.
    #     MaxX, MaxY = (500,800)
    #     DrawData = {}
    #
    #     # make some random rectangles
    #     l = []
    #     for i in range(5):
    #         w = random.randint(1,MaxX/2)
    #         h = random.randint(1,MaxY/2)
    #         x = random.randint(1,MaxX-w)
    #         y = random.randint(1,MaxY-h)
    #         l.append( (x,y,w,h) )
    #     DrawData["Rectangles"] = l
    #
    #     # make some random ellipses
    #     l = []
    #     for i in range(5):
    #         w = random.randint(1,MaxX/2)
    #         h = random.randint(1,MaxY/2)
    #         x = random.randint(1,MaxX-w)
    #         y = random.randint(1,MaxY-h)
    #         l.append( (x,y,w,h) )
    #     DrawData["Ellipses"] = l
    #
    #     # Polygons
    #     l = []
    #     for i in range(3):
    #         points = []
    #         for j in range(random.randint(3,8)):
    #             point = (random.randint(1,MaxX),random.randint(1,MaxY))
    #             points.append(point)
    #         l.append(points)
    #     DrawData["Polygons"] = l
    #
    #     return DrawData

# class ViewAreaSelectorPanel(BufferedWindow):
class ValuePickerScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel):

    def __init__(self,parent):
        self.parent = parent

class ViewAreaSelectorPanel(wx.Panel):
    xmin=0.0
    # xmax=.75
    ymin=0.0
    # ymax=.75
    vzoom=1.0
    viewer_loaded=False

    def __init__(self,parent,*args,**kwargs):

        wx.Panel.__init__(self,parent,*args,**kwargs)

        self.parent=parent
        # self.SetSize(wx.Size(500,300))
        # self.current_bitmap = wx.EmptyBitmapRGBA(10, 10, 255, 255, 255, 0)
        # BufferedWindow.__init__(self, parent)
        sz=self.GetSize()
        # self.set_box_coords()

        self.memdc = wx.MemoryDC(wx.NullBitmap)
        self.Bind(wx.EVT_PAINT, self.on_zoompanel_paint)
        self.Bind(wx.EVT_LEFT_DOWN,self.on_left_mouse_down)
        self.Bind(wx.EVT_LEFT_UP,self.on_left_mouse_up)
        self.Bind(wx.EVT_MOTION,self.on_mouse_motion)

        self.c = controller.Controller()
        self.c.set_zoompanel_reference(self)
        self.sz=sz

        self.Refresh()

    def set_box_coords(self,direct=False,xmin=None,ymin=None,vzoom=None,box_xmin=None,box_ymin=None,box_xmax=None,box_ymax=None):
        '''
        Direct here means setting it using the panel coordinates rather than the treespace coordinates
        :param direct:
        :param xmin:
        :param ymin:
        :param vzoom:
        :param box_xmin:
        :param box_ymin:
        :param box_xmax:
        :param box_ymax:
        :return:
        '''
        # print self.c.bw_aspect_ratio
        if direct==True:
            self.box_xmin=box_xmin
            self.box_xmax=box_xmax
            self.box_ymin=box_ymin
            self.box_ymax=box_ymax
            ar=abs((self.box_xmax-self.box_xmin)/(self.box_ymax-self.box_ymin))
            if ar>self.c.bw_aspect_ratio:
                self.box_ymax = self.box_ymin + (self.box_xmax-self.box_xmin)/self.c.bw_aspect_ratio
            else:
                self.box_xmax = self.box_xmin + (self.box_ymax - self.box_ymin)*self.c.bw_aspect_ratio

            xnew = np.dot(np.linalg.inv(self.trans_3x3),np.array([self.box_xmin,self.box_ymax,1],dtype=np.float64))
            xnew2 = np.dot(np.linalg.inv(self.trans_3x3), np.array([self.box_xmax, self.box_ymin, 1], dtype=np.float64))
            self.xmin=np.asscalar(xnew[0])
            self.ymin=np.asscalar(xnew[1])
            self.ymax = np.asscalar(xnew2[1])
            self.xmax = np.asscalar(xnew2[0])
            self.vzoom= (self.ymax-self.ymin)/self.v_zoom_full
            self.c.image_frame.m_statusBar2.SetStatusText("Direct: xmin: %s, xmax: %s, ymin: %s, ymax: %s" % (self.xmin,self.xmax,self.ymin,self.ymax),0)
        else:
            if xmin is not None:
                self.xmin=xmin
            if ymin is not None:
                self.ymin=ymin
            if vzoom is not None:
                self.vzoom=vzoom
            self.xmax=self.xmin+self.v_zoom_full*self.vzoom*self.c.bw_aspect_ratio
            self.ymax=self.ymin+self.v_zoom_full*self.vzoom
            mycoords=np.array(([self.xmin,self.xmax],
                               [self.ymin,self.ymax],
                               [1,1]),dtype=np.float64)
            outcoords=np.dot(self.trans,mycoords)
            # print self.trans
            self.box_xmin=np.asscalar(outcoords[0,0])
            self.box_xmax = np.asscalar(outcoords[0, 1])
            self.box_ymax= np.asscalar(outcoords[1,0])
            self.box_ymin = np.asscalar(outcoords[1,1])
            self.c.image_frame.m_statusBar2.SetStatusText(
                "Indirect: xmin: %s, xmax: %s, ymin: %s, ymax: %s" % (self.xmin, self.xmax, self.ymin, self.ymax), 0)






    def phylogeny_viewer_loaded(self):
        self.Bind(wx.EVT_SIZE, self.on_size_change)
        self.viewer_loaded=True
        self.xmin=self.c.buffered_window.top_left[0]
        self.ymin=self.c.buffered_window.bottom_right[1]
        self.v_zoom_full=abs(self.c.buffered_window.top_left[1]-self.c.buffered_window.bottom_right[1])
        self.sz=self.GetSize()
        self.set_global_bitmap()
        self.set_box_coords()
        self.Refresh()

    def on_left_mouse_down(self,event):
        ck=event.GetPosition()
        # print "click at (%s,%s)" % (ck[0],ck[1])
        self.sz=self.GetSize()
        # print "bounding box for click is (%s, %s, %s, %s)" % (self.box_xmin, self.box_xmax, self.box_ymin, self.box_ymax)
        if ck[0]<=self.box_xmax and ck[0]>=self.box_xmin and ck[1]>=self.box_ymin and ck[1]<=self.box_ymax:
            # print "click inside the bounding box"
            self.click=ck
            self.temp_xmin=self.box_xmin
            self.temp_xmax=self.box_xmax
            self.temp_ymin=self.box_ymin
            self.temp_ymax=self.box_ymax
            # print self.click
        else:
            self.click=None

    def on_left_mouse_up(self,event):
        self.clickup=event.GetPosition()
        if self.click!=None:
            offsetx=self.clickup[0]-self.click[0]
            offsety=self.clickup[1]-self.click[1]
            self.reset_view_square(offset=(offsetx,offsety))
            # print (offsetx,offsety)
            # self.box_xmin=self.xmin*float(self.sz[0])
            # self.box_xmax=(self.xmin+self.zoom)*float(self.sz[0])
            # self.box_ymin=(self.ymin)*float(self.sz[1])
            # self.box_ymax=(self.ymin+self.zoom)*float(self.sz[1])

        self.click=None
        self.clickup=None
        self.set_zoom_level(    )

    def reset_view_square(self,offset=None,zoom=None):
        if offset<>None:
            args={}
            args['box_xmin']=self.temp_xmin+offset[0]
            args['box_xmax']=self.temp_xmax+offset[0]
            args['box_ymin']=self.temp_ymin+offset[1]
            args['box_ymax']=self.temp_ymax+offset[1]
            self.set_box_coords(direct=True,**args)
            self.sz=self.GetSize()
            # CHANGE
            # self.xmin=(float(self.temp_xmin)+float(offset[0]))/float(self.sz[0])
            # self.xmax=self.temp_xmax+float(offset[0])/float(self.sz[0])
            # self.ymin=(float(self.temp_ymin)+float(offset[1]))/float(self.sz[1])
            # self.ymax=self.temp_ymax+float(offset[1])/float(self.sz[1])
            # print str((self.xmin,self.ymin))
            # if self.xmin<0:
            #     self.xmin=0
            # if self.xmin+self.zoom>1:
            #     self.xmax=1
                # self.xmin=1-self.zoom
            # if self.ymin<0:
            #     self.ymin=0
            #     self.ymax=h
            # if self.ymin+self.zoom>1:
            #     self.ymin=1-self.zoom
        # print str(offset) + "\t" + str(self.sz) + "\t" + str((self.xmin,self.xmax,self.ymin, self.ymax))
        # self.UpdateDrawing()
        self.Refresh()

    def reposition_view_square(self):
        # sz=self.GetSize()
        #CHANGE
        # self.box_xmin=self.xmin*float(sz[0])
        # self.box_xmax=self.box_xmin+self.zoom*float(sz[0])
        # self.box_ymin=self.ymin*float(sz[1])
        # self.box_ymax=self.box_ymin+self.zoom*float(sz[1])
        self.set_box_coords()


    def set_zoom_level(self,newzoom=None):
        if newzoom is not None:
            self.vzoom=newzoom
            self.set_box_coords()
        # print "bounding box after zoom is (%s, %s, %s, %s)" % (self.box_xmin, self.box_xmax, self.box_ymin, self.box_ymax)
        self.c.buffered_window.bottom_right=(self.xmax,self.ymin)
        self.c.buffered_window.top_left=(self.xmin,self.ymax)
        self.c.trigger_refresh()
        # self.v_zoom_full
        self.Refresh()
        self.Update()



    def on_mouse_motion(self,event):
        # print event.LeftIsDown()
        if event.LeftIsDown()==False or self.click==None:
            # print "left is down"
            self.click=None
            self.clickup=None
        else:
            self.clickup=event.GetPosition()
            offsetx = self.clickup[0]-self.click[0]
            offsety = self.clickup[1]-self.click[1]
            self.reset_view_square(offset=(offsetx,offsety))

    # def Draw(self,dc):
    #     self.sz=dc.GetSize()
    #
    #     dc.DrawBitmap(self.current_bitmap,0,0)
    #     col = wx.Colour(100, 100, 100, 0.5)
    #     br = wx.Brush(col, wx.TRANSPARENT)
    #     pn = wx.Pen(wx.Colour(255, 0, 0),2,wx.SOLID)
    #     x = int(self.sz[0] * self.xmin)
    #     y = int(self.sz[1] * self.ymin)
    #     h = int(self.sz[1] * (self.zoom))
    #     w = int(self.sz[0] * (self.zoom))
    #     dc.SetBrush(br)
    #     dc.SetPen(pn)
    #     dc.DrawRectangle(x,y,w,h)
    #     self.reposition_view_square()

    def on_zoompanel_paint(self,event):
        # print "painting"
        # pdc=wx.PaintDC(self)
        # pdc=wx.PaintDC(self)
        # pdc.SetBackground(wx.Brush("white"))
        # self.sz = pdc.GetSize()
        # print self.GetSize()
        # print self.sz
        # pdc.Clear()
        # pdc.DrawBitmap(self.current_bitmap,0,0,True)
        temp_image=wx.BitmapFromBuffer(self.current_bitmap.GetWidth(),self.current_bitmap.GetHeight(),self.imgbuffer)
        self.memdc.Clear()
        # print "cleared memdc"
        new_bitmap=wx.EmptyBitmap(*self.sz)
        self.memdc.SelectObject(new_bitmap)
        # print "memdc selected"

        self.memdc.DrawBitmap(temp_image,0,0)

        # pdc.DrawBitmap(self.current_bitmap, 0, 0, False)
        # pdc.DrawBitmap(wx.BitmapFromImage(self.myimg,3),0,0)
        # pdc.DrawBitmap(wx.Bitmap(my_globals.amato_qiime_root + 'test.jpg', wx.BITMAP_TYPE_JPEG),1,1)

        # pdc.DrawLineList(self.line_list)
        # self.Update()
        # self.pdc.DrawBitmap(self.current_bitmap, round(self.sz[1]/2.0,0), round(self.sz[0]/2.0,0))
        # col=wx.Colour(171,171,171,100)
        col=wx.Colour(100,100,100,0.5)
        br=wx.Brush(col,wx.TRANSPARENT)
        pn=wx.Pen(wx.Colour(0,0,0))
        # self.sz=self.pdc.GetSize()
        # print self.sz
        # x=int(self.sz[0]*self.xmin)
        # y=int(self.sz[1]*self.ymin)
        # h=int(self.sz[1]*(self.zoom))
        # w=int(self.sz[0]*(self.zoom))
        # print (x,y,h,w)
        self.memdc.SetBrush(br)
        self.memdc.SetPen(pn)
        # print "memdc brushpen"
        # print "at paint: bxmin: %s, bxmax: %s, bymin: %s, bymax: %s" % ( self.box_xmin,self.box_xmax, self.box_ymin, self.box_ymax)
        self.memdc.DrawRectangle(self.box_xmin,self.box_ymin,abs(self.box_xmax-self.box_xmin),abs(self.box_ymax-self.box_ymin))
        # print "drew rectangle"
        self.memdc.SelectObject(wx.NullBitmap)
        dc=wx.BufferedPaintDC(self)
        dc.DrawBitmap(new_bitmap,0,0)
        # self.reposition_view_square()
        # self.Refresh()
        # self.parent.Update()

    # def OnSize(self,event):
    #     # The Buffer init is done here, to make sure the buffer is always
    #     # the same size as the Window
    #     Size  = self.GetClientSizeTuple()
    #
    #
    #     # Make new offscreen bitmap: this bitmap will always have the
    #     # current drawing in it, so it can be used to save the image to
    #     # a file, or whatever.
    #     self._Buffer = wx.EmptyBitmapRGBA(Size[0],Size[1],255,255,255,wx.ALPHA_OPAQUE)
    #     if self.viewer_loaded==True:
    #         self.set_global_bitmap()
    #     self.UpdateDrawing()


    def on_size_change(self,event=None):
        self.sz=self.GetSize()
        self.set_global_bitmap()


    def set_global_bitmap(self):
        drawdata=self.c.buffered_window.DrawData['segments']
        theta=float(self.c.buffered_window.rotation)/360.0 * 2 * math.pi
        self.global_bounding_box=[0.0,0.0,0.0,0.0]  #(xmin, xmax, ymin, ymax)
        npdrawdata=np.zeros((len(drawdata),6),dtype=np.float64)
        for ind in range(len(drawdata)):
            i=drawdata[ind]
            npdrawdata[ind,:] = [i[0]*math.cos(theta)-i[1]*math.sin(theta),i[0]*math.sin(theta)+i[1]*math.cos(theta),1.0,
                                 i[2] * math.cos(theta) - i[3] * math.sin(theta), i[2] * math.sin(theta) + i[3] * math.cos(theta),1.0]
        maxes=np.amax(npdrawdata,0)
        mins=np.amin(npdrawdata,0)
        xmax = max(np.asscalar(maxes[0]),np.asscalar(maxes[3]))
        ymax = max(np.asscalar(maxes[1]), np.asscalar(maxes[4]))
        xmin = min(np.asscalar(mins[0]), np.asscalar(mins[3]))
        ymin = min(np.asscalar(mins[1]), np.asscalar(mins[4]))
        self.global_bounding_box=[xmin-.00001,xmax+.00001,ymin-.00001,ymax+.00001]

        # print self.global_bounding_box
        bb_aspect = abs((xmax-xmin)/(ymax-ymin))
        h=float(self.sz[1])
        w=float(self.sz[0])
        my_aspect = w/h

        if bb_aspect>my_aspect:
            #bb width is the constaint, so expand the height
            gap = 1.0/my_aspect*(xmax-xmin)-(ymax-ymin)
            self.global_bounding_box[2]=ymin-gap/2.0
            self.global_bounding_box[3]=ymax+gap/2.0
        else:
            #bb height is the constraint, so expand the width
            gap = my_aspect*(ymax - ymin) - (xmax-xmin)
            self.global_bounding_box[0] = xmin - gap/2.0
            self.global_bounding_box[1] = xmax + gap/2.0

        a=np.array(([self.global_bounding_box[0],self.global_bounding_box[2],1],
                   [self.global_bounding_box[0], self.global_bounding_box[3], 1],
                   [self.global_bounding_box[1],self.global_bounding_box[3],1]),dtype=np.float64)
        ainv = np.linalg.inv(a)
        tx = np.dot(ainv,np.array([0,0,w-1],dtype=np.float64))
        ty = np.dot(ainv,np.array([h-1,0,0],dtype=np.float64))
        self.trans = np.vstack((tx,ty))
        self.trans_3x3=np.vstack((tx,ty,np.array([0,0,1],dtype=np.float64)))
        self.pts = np.hstack((np.dot(npdrawdata[:,0:3],self.trans.transpose()),np.dot(npdrawdata[:,3:6],self.trans.transpose())))
        # print self.pts[0:50,:]
        self.line_list=[]
        for i in range(len(drawdata)):
            self.line_list.append((round(np.asscalar(self.pts[i,0]),0),round(np.asscalar(self.pts[i,1]),0),
                                   round(np.asscalar(self.pts[i, 2]), 0),round(np.asscalar(self.pts[i,3]),0)))
        # for i in self.line_list[0:5]:
        #     print i
        # self.memdc.Clear()
        # self.current_bitmap=wx.EmptyBitmapRGBA(self.sz[0],self.sz[1],255,255,255,wx.ALPHA_OPAQUE)
        self.sz=self.GetSize()
        self.current_bitmap = wx.EmptyBitmapRGBA(self.sz[0], self.sz[1], 255, 255, 255,wx.ALPHA_OPAQUE)
        # self.current_bitmap = wx.EmptyBitmap(self.sz[0], self.sz[1])
        self.memdc.Clear()
        self.memdc.SelectObject(self.current_bitmap)
        self.memdc.SetPen(wx.Pen(wx.Colour(0,0,0,255),1,wx.SOLID))
        self.memdc.DrawLineList(self.line_list)
        # self.memdc.SetBrush(wx.Brush(wx.BLUE,wx.SOLID))
        # self.memdc.DrawCircle(200,200,50)
        self.memdc.SelectObject(wx.NullBitmap)
        self.imgbuffer = bytearray(self.sz[0]*self.sz[1]*3)
        self.current_bitmap.CopyToBuffer(self.imgbuffer)

        # self.UpdateDrawing()
        self.myimg=self.current_bitmap.ConvertToImage()
        # self.myimg.SaveFile(my_globals.amato_qiime_root + 'test.jpg',wx.BITMAP_TYPE_JPEG)


# class MyPopupMenu(wx.Menu):
#     def __init__(self, parent, point):
#         wx.Menu.__init__(self)
#         self.phylo_bw = parent
#         self.pt = point
#
#         itemAddTxt = wx.MenuItem(self, wx.NewId(), "Add Text Annotation Here")
#         self.AppendItem(itemAddTxt)
#         self.Bind(wx.EVT_MENU, self.OnAddText, itemAddTxt)
#
#         item = wx.MenuItem(self, wx.NewId(), "Item Two")
#         self.AppendItem(item)
#         self.Bind(wx.EVT_MENU, self.OnItem2, item)
#
#         item = wx.MenuItem(self, wx.NewId(), "Item Three")
#         self.AppendItem(item)
#         self.Bind(wx.EVT_MENU, self.OnItem3, item)
#
#     def OnAddText(self, event):
#         ad=AddTxtDialog().ShowModal()
#
#
#         print "Item One selected in the %s window" % self.WinName
#
#     def OnItem2(self, event):
#         print "Item Two selected in the %s window" % self.WinName
#
#     def OnItem3(self, event):
#         print "Item Three selected in the %s window" % self.WinName

