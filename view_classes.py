__author__ = 'Michael'
import wx
import random, colorsys
import controller
import aux_view_classes as avc

global colors

def get_random_color(incr=None):
    if incr is None:
        H=random.random()
    else:
        H=incr+.03+random.random()*.08
    while True:
        S=random.random()*.5 + .5
        V=random.random()*.5 + .5
        if S+V>1.5:
            break
    rgb=colorsys.hsv_to_rgb(H,S,V)
    return rgb

colors=[(240,163,255),(0,117,220),(153,63,0),(76,0,92),(25,25,25),(0,92,49),(43,206,72),(255,204,153),(128,128,128),(148,255,181),(143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),(255,168,187),(66,102,0),(255,0,16),(94,241,242),(0,153,143),(224,255,102),(116,10,255),(153,0,0),(255,255,128),(255,255,0),(255,80,5)]

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
            if k>len(colors):
                clr=get_random_color()
            else:
                clr=colors[k]
                k+=1
            self.colors[i]=clr


            a=self.ValuePicker(self.parent,i,clr,val_ctrl=self)
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
            vp=self.ValuePicker(**i)
            self.Add(vp,0, wx.EXPAND,5)
            self.value_pickers.append(vp)
        self.add_final_spacer()
        self.Layout()

    class ValuePicker(wx.BoxSizer):
        def __init__(self,parent=None, value=None,clr=None, sz=2, checked=False, val_ctrl=None):
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
            self.c.update_cirlces_by_annotation()
            self.c.trigger_refresh()

        def process_color_change(self,event):
            newcolor=self.m_colourPicker1.GetColour()
            self.clr=newcolor.Get()
            self.c.update_cirlces_by_annotation()
            self.c.trigger_refresh()

        def process_size_change(self,event):
            print "processing size change"
            self.size=int(self.m_spinCtrl.GetValue())
            self.c.update_cirlces_by_annotation()
            self.c.trigger_refresh()


class ViewAreaSelectorPanel(wx.Panel):
    xmin=.25
    # xmax=.75
    ymin=.25
    # ymax=.75
    zoom=.5

    def __init__(self,parent,*args,**kwargs):
        wx.Panel.__init__(self,parent,*args,**kwargs)
        self.parent=parent
        # self.SetSize(wx.Size(500,300))
        sz=self.GetSize()
        self.box_xmin=self.xmin*float(sz[0])
        self.box_xmax=(self.xmin+self.zoom)*float(sz[0])
        self.box_ymin=(self.ymin)*float(sz[1])
        self.box_ymax=(self.ymin+self.zoom)*float(sz[1])


        self.current_bitmap=wx.EmptyBitmapRGBA(sz[0],sz[1],255,255,255,0)
        self.Bind(wx.EVT_PAINT, self.on_zoompanel_paint)
        self.Bind(wx.EVT_LEFT_DOWN,self.on_left_mouse_down)
        self.Bind(wx.EVT_LEFT_UP,self.on_left_mouse_up)
        self.Bind(wx.EVT_MOTION,self.on_mouse_motion)
        self.c = controller.Controller()
        self.sz=None

    def on_left_mouse_down(self,event):
        ck=event.GetPosition()
        self.sz=self.GetSize()
        if ck[0]<=self.box_xmax and ck[0]>=self.box_xmin and ck[1]>=self.box_ymin and ck[1]<=self.box_ymax:
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
            self.reposition_view_square()
            # print (offsetx,offsety)
            self.box_xmin=self.xmin*float(self.sz[0])
            self.box_xmax=(self.xmin+self.zoom)*float(self.sz[0])
            self.box_ymin=(self.ymin)*float(self.sz[1])
            self.box_ymax=(self.ymin+self.zoom)*float(self.sz[1])

        self.click=None
        self.clickup=None

    def reset_view_square(self,offset=None,zoom=None):
        if offset<>None:
            self.sz=self.GetSize()
            self.xmin=(float(self.temp_xmin)+float(offset[0]))/float(self.sz[0])
            # self.xmax=self.temp_xmax+float(offset[0])/float(self.sz[0])
            self.ymin=(float(self.temp_ymin)+float(offset[1]))/float(self.sz[1])
            # self.ymax=self.temp_ymax+float(offset[1])/float(self.sz[1])
            # print str((self.xmin,self.ymin))
            if self.xmin<0:
                self.xmin=0
            if self.xmin+self.zoom>1:
                # self.xmax=1
                self.xmin=1-self.zoom
            if self.ymin<0:
                self.ymin=0
                # self.ymax=h
            if self.ymin+self.zoom>1:
                self.ymin=1-self.zoom
        # print str(offset) + "\t" + str(self.sz) + "\t" + str((self.xmin,self.xmax,self.ymin, self.ymax))
        self.Refresh()

    def reposition_view_square(self):
        sz=self.GetSize()
        self.box_xmin=self.xmin*float(sz[0])
        self.box_xmax=self.box_xmin+self.zoom*float(sz[0])
        self.box_ymin=self.ymin*float(sz[1])
        self.box_ymax=self.box_ymin+self.zoom*float(sz[1])


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


    def on_zoompanel_paint(self,event):
        # print "painting"
        self.pdc=wx.PaintDC(self)
        self.pdc.DrawBitmap(self.current_bitmap,0,0)
        # col=wx.Colour(171,171,171,100)
        col=wx.Colour(100,100,100,0.5)
        br=wx.Brush(col,wx.TRANSPARENT)
        self.sz=self.pdc.GetSize()
        # print sz
        x=int(self.sz[0]*self.xmin)
        y=int(self.sz[1]*self.ymin)
        h=int(self.sz[1]*(self.zoom))
        w=int(self.sz[0]*(self.zoom))
        # print (x,y,h,w)
        self.pdc.SetBrush(br)
        self.pdc.DrawRectangle(x,y,w,h)

    def get_parent_bitmap(self):
        cim=wx.ImageFromBitmap(self.c.get_current_bitmap())
        bigsize=cim.GetSize()
        if bigsize[0]>bigsize[1]:
            my_w=500
            my_h=round(float(bigsize[1])/float(bigsize[0])*500.0)
            # print bigsize[0]
            # print bigsize[1]
            # print bigsize[1]/bigsize[0]*500
        else:
            my_h=500
            my_w=round(float(bigsize[0])/float(bigsize[1])*500.0)
        # print (my_w,my_h)
        self.SetSize(wx.Size(my_w,my_h))
        self.Layout()
        self.c.view_layout_main_frame()
        # self.Refresh()
        # self.memdc=wx.MemoryDC(self.current_bitmap)
        # sz=self.memdc.GetSize()
        self.current_bitmap=wx.BitmapFromImage(cim.Rescale(my_w,my_h))
        # self.memdc.SelectObject(wx.NullBitmap)


class zoom_rotation_ctrl(avc.zoom_rotation_control):
    def __init__(self,parent,*args,**kwargs):
        avc.zoom_rotation_control(parent,*args,**kwargs)
