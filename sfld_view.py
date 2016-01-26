# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class imgFrame
###########################################################################

class imgFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1058,759 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.img_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.FULL_REPAINT_ON_RESIZE|wx.TAB_TRAVERSAL )
		self.img_panel.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.img_panel.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer1.Add( self.img_panel, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.img_panel.Bind( wx.EVT_PAINT, self.OnImgPaint )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnImgPaint( self, event ):
		event.Skip()
	

###########################################################################
## Class ctrlFrame
###########################################################################

class ctrlFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 513,370 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		self.m_panel2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFile = wx.StaticText( self.m_panel2, wx.ID_ANY, u"File", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lblFile.Wrap( -1 )
		self.lblFile.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.lblFile.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer4.Add( self.lblFile, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_filePicker1 = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer4.Add( self.m_filePicker1, 1, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFile1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Metadata", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lblFile1.Wrap( -1 )
		self.lblFile1.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.lblFile1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer5.Add( self.lblFile1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_filePicker11 = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer5.Add( self.m_filePicker11, 1, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button1 = wx.Button( self.m_panel2, wx.ID_ANY, u"SaveFile", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button1, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer6, 0, 0, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer3.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer3 )
		self.m_panel2.Layout()
		bSizer3.Fit( self.m_panel2 )
		bSizer2.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_filePicker1.Bind( wx.EVT_FILEPICKER_CHANGED, self.set_file )
		self.m_filePicker11.Bind( wx.EVT_FILEPICKER_CHANGED, self.set_file )
		self.m_button1.Bind( wx.EVT_LEFT_UP, self.SaveCurrentImage )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def set_file( self, event ):
		event.Skip()
	
	
	def SaveCurrentImage( self, event ):
		event.Skip()
	

