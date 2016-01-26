__author__ = 'Michael'

from my_globals import *
import tree_manipulator as trman
import sfld_view
import wx
import skimage.io
import skimage.transform
import skimage.draw
import numpy as np


class MyApp(wx.App):
    def OnInit(self):
        self.mainframe = gui_manager(None)
        self.SetTopWindow(self.mainframe)
        self.mainframe.Show()

        return True



class gui_manager(sfld_view.ctrlFrame):
    '''
    top level frame for this application
    '''
    def __init__(self,parent):
        sfld_view.ctrlFrame.__init__(self,parent)
        self.image_frame=image_manager(self)
        self.image_frame.Show()
        # self.image_frame.drawwhatever()

    def SaveCurrentImage(self,event):
        self.image_frame.save_dc_to_bitmap()

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

        print 'opening tree file & making phylogram'
        self.rp=trman.Radial_Phylogram(test_tp)
        self.rp.get_max_dims()
        self.rp.get_segments()
        self.current_bitmap=None

    def save_dc_to_bitmap(self):
        self.current_bitmap.SaveFile(test_folder + '/wx_output_bitmap.jpg',wx.BITMAP_TYPE_JPEG)


    def OnImgPaint(self,event):
        # self.dc=wx.PaintDC(self.img_panel)
        self.pdc=wx.PaintDC(self.img_panel)
        w=self.pdc.GetSize()[0]
        h=self.pdc.GetSize()[1]
        self.get_current_tree_image(w,h)
        self.pdc.DrawBitmap(self.current_bitmap,0,0)

    def get_current_tree_image(self,w,h):
        self.current_bitmap=wx.EmptyBitmap(w,h)
        self.memdc=wx.MemoryDC(self.current_bitmap)
        # self.dc.DrawBitmap(self.testimage(),0,0)
        # self.drawwhatever(self.dc)
        self.memdc.Clear()
        print 'drawing phylogram'
        sz=(w,h)
        print sz
        oldrange=self.rp.max_dims
        print oldrange

        for i in self.rp.segments:
            # print i[0]
            # print i[1]
            x1=convert_coordinates(oldrange,sz,i[0])
            x2=convert_coordinates(oldrange,sz,i[1])
            # if x2[0]>xma:
            #     xma=x2[0]
            # if x2[1]>yma:
            #     yma=x2[1]
            if x1 is not None and x2 is not None:
                self.memdc.DrawLine(x1[0],x1[1],x2[0],x2[1])

        self.memdc.SelectObject(wx.NullBitmap)
        # self.current_bitmap=self.dc.GetAsBitmap()
        # print (xma,yma)

    def drawwhatever(self,dc):
        dc.DrawLine(1,1,50,50)

    # def testimage(self):
    #     ti=skimage.io.imread(test_image)
    #     h=int(ti.shape[0])
    #     w=int(ti.shape[1])
    #     print h
    #     print w
    #     wxi=wx.ImageFromBuffer(w,h,np.getbuffer(ti))
    #     wxb=wxi.ConvertToBitmap()
    #     return wxb

# class DisplayImage():
#     treepath=test_tp
#     #initial dimensions:
#     w=5000
#     h=3000
#
#     def __init__(self):
#         self.rp=trman.Radial_Phylogram(self.treepath)
#         self.im=np.ones((self.w, self.h, 3),dtype='uint8')*255
#         self.maxdim=self.rp.get_max_dims()
#
#     def convert_coordinates(self):
#         horiz_span=self.maxdim[1]-self.maxdim[0]
#         vert_span=self.maxdim[3]-self.maxdim[2]




