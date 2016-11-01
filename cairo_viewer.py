__author__ = 'Michael'
import wx, os.path
import wx.lib.scrolledpanel
from wx.lib.delayedresult import startWorker
# import pickle, colorsys, random
import dendropy
# import controller
# import aux_view_classes as avc
# from view import *
# import my_globals
import numpy as np
global colors
import tree_manipulator as tm
from utilities import *
from view_classes import BufferedWindow
import cairo

class DrawPanelDBT(wx.Panel):
    """
    Complex panel with its content drawn in another thread
    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.t = None
        self.w, self.h = self.GetClientSizeTuple()
        self.buffer = wx.EmptyBitmap(self.w, self.h)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

        self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32,self.w, self.h)
        self.ctx = cairo.Context(self.surf)
        self.ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        self.ctx.rectangle(0,0,self.w, self.h)
        self.ctx.fill()

        self.SizeUpdate()

    #-------------------------------------------------------------------------
    def OnPaint(self, event=None):
        # Just draw prepared bitmap
        wx.BufferedPaintDC(self, self.buffer)
        # wx.BufferedPaintDC(self, self.surf.get_data())

    #-------------------------------------------------------------------------
    def OnSize(self, event):
        self.w, self.h = self.GetClientSizeTuple()
        self.buffer = wx.EmptyBitmap(self.w, self.h)
        self.Refresh()
        self.Update()
        # After drawing empty bitmap start update
        self.SizeUpdate()

    #-------------------------------------------------------------------------
    def OnEraseBackground(self, event):
        pass # Or None

    #-------------------------------------------------------------------------
    def OnTimer(self, event):
        # Start another thread which will update the bitmap
        # But only if another is not still running!
        if self.t is None:
            self.timer.Stop()
            self.t = startWorker(self.ComputationDone, self.Compute)

    #-------------------------------------------------------------------------
    def SizeUpdate(self):
        # The timer is used to wait for last thread to finish
        self.timer.Stop()
        self.timer.Start(100)

    def Compute(self):
        # self.ctx.move_to(300,100)
        self.ctx.new_sub_path()
        self.ctx.set_source_rgba(1. ,0. ,0., .5)
        self.ctx.arc(300,300,50,0,2*math.pi)
        self.ctx.fill()
        temp_buffer = wx.BitmapFromBufferRGBA(self.w, self.h, self.surf.get_data())
        return temp_buffer

    # -------------------------------------------------------------------------
    def ComputationDone(self, r):
        # When done, take bitmap and place it to the drawing buffer
        # Invalidate panel, so it is redrawn
        # But not if the later thread is waiting!
        temp = r.get()
        if not self.timer.IsRunning():
            self.buffer = temp
            self.Refresh()
            self.Update()
        self.t = None

class PhylogenyBufferedWindow(BufferedWindow):
    active_edge = None
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
        self.parent.m_statusBar2.SetStatusText("head: %s, %s |tail: %s, %s| len: %s" % (eref[0].head_node.label,
                                                                                        pos1, eref[0].tail_node.label,
                                                                                          pos2, eref[1]),2)
        self.active_edge=eref[0]
        self.activate_edge(eref[0])


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

    def on_clear_extra(self,event=None):
        self.active_edge = None
        self.parent.control_panel.m_textCtrl33.SetValue("None")
        self.ClearExtraDrawSegments()
        self.UpdateDrawing()

    def reroot_above_active_edge(self):
        if self.active_edge is not None:
            self.radial_phylogram.myt.reroot_at_edge(self.active_edge)
            self.radial_phylogram.refresh_all()
            self.MakeDrawData()

    def activate_edge(self,ed, pos1=None, pos2=None):
        self.active_edge = ed
        self.parent.control_panel.m_textCtrl33.SetValue(
            "head: %s, %s |tail: %s, %s| len: %s" % (ed.head_node.label,
                                                     pos1, ed.tail_node.label,
                                                     pos2, ed))
        self.parent.control_panel.m_textCtrl331.SetValue(str(self.radial_phylogram.node_labels[ed.head_node.label]['w']))
        self.parent.control_panel.m_textCtrl3311.SetValue(str(self.radial_phylogram.node_labels[ed.head_node.label]['t']))

    def deactivate_edge(self):
        self.active_edge = None
        self.parent.control_panel.m_textCtrl33.SetValue("None")
        self.parent.control_panel.m_textCtrl331.SetValue("")
        self.parent.control_panel.m_textCtrl3311.SetValue("")

    def adjust_tree(self):
        if self.active_edge is not None:
            width_radians = float(self.parent.control_panel.m_textCtrl331.GetValue())
            right_edge_radians = float(self.parent.control_panel.m_textCtrl3311.GetValue())
            self.radial_phylogram.deform_clade_by_wedge_and_radians(self.active_edge,width_radians,right_edge_radians)
            self.MakeDrawData(False)
            self.UpdateDrawing()
        else:
            print "active edge not set! Tree not adjusted."


    def on_right_click( self, event ):
        # print "mouse_clicked"
        menu = MyContextMenu(self, event.GetPosition())
        self.PopupMenu(menu, event.GetPosition())
        menu.Destroy()
        # self.parent.m_statusBar2.SetStatusText("x: %s, y: %s" % event.GetPositionTuple(),1)

    def import_new_tree(self,treepath):
        if self.radial_phylogram is not None:
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




    def MakeDrawData(self, initial=True):
        self.radial_phylogram.get_leaf_node_coords()
        self.DrawData['segments']=[]

        for i in self.radial_phylogram.segments:
            self.DrawData['segments'].append((i[0][0],i[0][1],i[1][0],i[1][1]))
        max_dims=self.radial_phylogram.get_max_dims()
        if initial==True:
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
        jr = my_globals.jitter_radius
        curr_brush = dc.GetBrush()
        curr_pen = dc.GetPen()
        if circle_set is None:
            circle_set = self.ExtraDrawCircles
        for i in circle_set:
            x=self.transform_coordinate(i[0])
            if self.parent.control_panel.m_checkBox6.IsChecked():
                y = (float(x[0] + (random.random() - .5) / .5 * jr), float(x[1] + (random.random() - .5) / .5 * jr))
                x = (int(y[0]), int(y[1]))
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

    def DrawCairoFigure(self,event=None):
        print "Not using CairoBufferedWindow"
