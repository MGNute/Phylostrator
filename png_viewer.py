import time, sys
import wx
import sfld_view, controller
from view_classes import BufferedWindow
import os.path
import threading

class PNGBufferedWindow(BufferedWindow):
    def __init__(self,parent,imagepath=None,*args, **kwargs):
        self.parent=parent
        if imagepath==None:
            # self.image_path='C:\\Users\\miken\\Grad School Stuff\\Research\\Phylogenetics\\Metagenomics\\stumpf\\example.png'
            self.image_path='resources/temp.png'
        else:
            self.image_path=imagepath
        self.image = None
        self.mod_time = 0.0
        self.white_background = False
        BufferedWindow.__init__(self,parent, *args, **kwargs)
        # self.SetForegroundColour( wx.Colour( 255, 255, 255,0 ) )
        # self.SetBackgroundColour( wx.Colour( 255, 255, 255,0 ) )
        self.SetForegroundColour(wx.WHITE)
        self.SetBackgroundColour(wx.WHITE)

        self.daem = threading.Thread(target=self.check_mod_time)
        self.daem.setDaemon(True)
        self.daem.start()
        self.Bind(wx.EVT_RIGHT_DCLICK, self.on_right_dclick)

    def check_mod_time(self):
        while True:
            tm = os.path.getmtime(self.image_path)
            if tm > self.mod_time:
                self.parent.set_status('reloading image...')
                wx.CallAfter(self.load_image)
                time.sleep(1)
                self.parent.set_status('')
            time.sleep(1)

    def on_right_dclick(self,event):
        print event.GetPosition()

    def set_image_path(self,image_path):
        self.image_path=image_path

    def load_image(self):
        del self.image
        try:
            self.image = wx.Bitmap(name=self.image_path,type=wx.BITMAP_TYPE_PNG)
        except:
            time.sleep(1)
            self.image = wx.Bitmap(name=self.image_path, type=wx.BITMAP_TYPE_PNG)
        self.mod_time = os.path.getmtime(self.image_path)
        self.UpdateDrawing()

    def Draw(self,dc):
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        if self.white_background==True:
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.SetPen(wx.WHITE_PEN)
            sz = dc.GetSizeTuple()
            dc.DrawRectangle(0,0,sz[0],sz[1])
        if self.image <> None:
            dc.DrawBitmap(self.image,0,0)

        # print str(self.GetBackgroundColour())

class pngviewer(sfld_view.imgFrame):
    def __init__(self,parent):
        sfld_view.imgFrame.__init__(self,parent)

        # initialize controller and other misc
        self.sz=None

        # add window
        # self.img_panel=view_classes.BufferedWindow
        self.make_image_panel()
        self.m_filePicker5 = wx.FilePickerCtrl(self.m_toolBar1, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                               wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        self.m_toolBar1.AddControl(self.m_filePicker5)
        self.m_toolBar1.Realize()

        # bind methods
        self.img_panel.Bind(wx.EVT_RIGHT_DCLICK,self.right_dclick)
        self.m_filePicker5.Bind(wx.EVT_FILEPICKER_CHANGED, self.chg_file)

        if len(sys.argv)>1:
            self.m_filePicker5.SetPath(sys.argv[1])


    def right_dclick(self, event):
        print event.GetPosition()

    def chg_file(self,event=None):
        fi=self.m_filePicker5.GetPath()
        self.img_panel.image_path=fi
        self.img_panel.UpdateDrawing()

    def make_image_panel(self):
        self.bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.img_panel = PNGBufferedWindow(self)
        # self.img_panel.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        # self.img_panel.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        self.bSizer1.Add( self.img_panel, 1, wx.EXPAND, 0 )
        self.SetSizer( self.bSizer1 )
        self.Layout()

    def set_status(self,msg):
        self.m_statusBar2.SetStatusText(msg)


class PngViewerApp(wx.App):
    def OnInit(self):
        self.mainframe = pngviewer(None)
        self.SetTopWindow(self.mainframe)
        self.mainframe.SetIcon(wx.Icon('resources/icnPhyloMain32.png'))
        self.mainframe.Show()
        return True

if __name__ == '__main__':
    app = PngViewerApp()
    app.MainLoop()