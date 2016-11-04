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
from view_classes import PhylogenyBufferedWindow, MyContextMenu
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
