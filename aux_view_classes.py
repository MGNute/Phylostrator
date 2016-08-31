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
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )
		
		
		bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
		
		
		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class zoom_rotation_control
###########################################################################

class zoom_rotation_control ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,39 ), style = wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
		
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Zoom:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer3.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer3.AddSpacer( ( 5, 0), 0, 0, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"+ ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( 18, 74, 90, 92, False, "Arial" ) )
		self.m_staticText2.SetToolTipString( u"Zoom In" )
		
		bSizer3.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )
		self.m_textCtrl2.SetMaxSize( wx.Size( 30,-1 ) )
		
		bSizer3.Add( self.m_textCtrl2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"%", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		bSizer3.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u" -", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		self.m_staticText21.SetFont( wx.Font( 18, 74, 90, 92, False, "Arial" ) )
		self.m_staticText21.SetToolTipString( u"Zoom Out" )
		
		bSizer3.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		
		bSizer3.AddSpacer( ( 20, 0), 0, 0, 5 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer3.AddSpacer( ( 20, 0), 0, wx.EXPAND, 5 )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Rotation:  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer3.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, u"+ ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		self.m_staticText22.SetFont( wx.Font( 18, 74, 90, 92, False, "Arial" ) )
		
		bSizer3.Add( self.m_staticText22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.m_textCtrl21 = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl21.SetMaxSize( wx.Size( 30,-1 ) )
		
		bSizer3.Add( self.m_textCtrl21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"°", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
		
		bSizer3.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.m_staticText211 = wx.StaticText( self, wx.ID_ANY, u" -", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText211.Wrap( -1 )
		self.m_staticText211.SetFont( wx.Font( 18, 74, 90, 92, False, "Arial" ) )
		
		bSizer3.Add( self.m_staticText211, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		# Connect Events
		self.m_staticText2.Bind( wx.EVT_LEFT_DOWN, self.zoom_in )
		self.m_textCtrl2.Bind( wx.EVT_TEXT, self.adjust_zoom )
		self.m_staticText21.Bind( wx.EVT_LEFT_DOWN, self.zoom_out )
		self.m_staticText22.Bind( wx.EVT_LEFT_DCLICK, self.rotate_minus_counterclock )
		self.m_textCtrl21.Bind( wx.EVT_TEXT, self.adjust_rotation )
		self.m_textCtrl21.Bind( wx.EVT_TEXT_ENTER, self.adjust_rotation )
		self.m_staticText211.Bind( wx.EVT_LEFT_DCLICK, self.rotate_plus_clockwise )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def zoom_in( self, event ):
		event.Skip()
	
	def adjust_zoom( self, event ):
		event.Skip()
	
	def zoom_out( self, event ):
		event.Skip()
	
	def rotate_minus_counterclock( self, event ):
		event.Skip()
	
	def adjust_rotation( self, event ):
		event.Skip()
	
	
	def rotate_plus_clockwise( self, event ):
		event.Skip()
	

