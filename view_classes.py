__author__ = 'Michael'
import wx
import random, colorsys
import controller

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
        self.set_values(['189'])


    def set_values(self,vals):
        self.Clear(True)
        self.values=vals
        self.value_pickers=[]
        k=0

        self.colors={}
        for i in self.values:
            if k>len(colors):
                clr=get_random_color()
            else:
                clr=colors[k]
                k+=1
            self.colors[i]=clr


            a=self.ValuePicker(self.parent,i,clr)
            self.Add(a,0, wx.EXPAND, 5)
            self.value_pickers.append(a)

        self.add_final_spacer()

    def add_final_spacer(self):
        bSizer15 = wx.BoxSizer( wx.VERTICAL )
        bSizer15.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        self.Add( bSizer15, 1, wx.EXPAND, 5 )


    class ValuePicker(wx.BoxSizer):
        def __init__(self,parent, value,clr, checked=False):
            self.c=controller.Controller()
            self.parent=parent
            self.value=value
            self.clr=clr
            wx.BoxSizer.__init__(self,wx.HORIZONTAL)
            self.m_checkBox1 = wx.CheckBox(parent, wx.ID_ANY, value, wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_checkBox1.SetValue(False)
            self.Add( self.m_checkBox1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

            self.m_colourPicker1 = wx.ColourPickerCtrl(parent, wx.ID_ANY, wx.Colour(clr[0],clr[1],clr[2]), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
            self.Add( self.m_colourPicker1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

            self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.process_annotationvalue_check )
            self.m_colourPicker1.Bind( wx.EVT_COLOURPICKER_CHANGED, self.process_color_change )

        def process_annotationvalue_check(self,event):
            self.c.update_cirlces_by_annotation()
            self.c.trigger_refresh()

        def process_color_change(self,event):
            newcolor=self.m_colourPicker1.GetColour()
            self.clr=newcolor.Get()
            self.c.update_cirlces_by_annotation()
            self.c.trigger_refresh()