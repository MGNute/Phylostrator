# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.propgrid as pg
import wx.grid

###########################################################################
## Class imgFrame
###########################################################################

class imgFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Phylostrator", pos = wx.DefaultPosition, size = wx.Size( 1500,800 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_statusBar2 = self.CreateStatusBar( 3, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.icnControlPanel = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/icnControls30.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Control Panel", u"Show/Hide the Control Panel", None ) 
		
		self.m_toolBar1.Realize() 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_LEFT_DOWN, self.on_click )
		self.Bind( wx.EVT_RIGHT_DOWN, self.on_right_click )
		self.Bind( wx.EVT_TOOL, self.control_panel_tool_click, id = self.icnControlPanel.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_click( self, event ):
		event.Skip()
	
	def on_right_click( self, event ):
		event.Skip()
	
	def control_panel_tool_click( self, event ):
		event.Skip()
	

###########################################################################
## Class ctrlFrame
###########################################################################

class ctrlFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"SFLD Tree Viewer - Controls", pos = wx.Point( 1,1 ), size = wx.Size( 886,750 ), style = wx.DEFAULT_FRAME_STYLE|wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.m_notebook1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		self.m_panel2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFile2 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Config File", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lblFile2.Wrap( -1 )
		self.lblFile2.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.lblFile2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer41.Add( self.lblFile2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer41.AddSpacer( ( 43, 0), 0, wx.EXPAND, 5 )
		
		self.m_FilePicker_config = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 500,-1 ), wx.FLP_DEFAULT_STYLE )
		self.m_FilePicker_config.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer41.Add( self.m_FilePicker_config, 0, wx.ALL, 5 )
		
		self.btn_import_tree1 = wx.Button( self.m_panel2, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.btn_import_tree1, 0, wx.ALL, 5 )
		
		self.m_checkBox51 = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Use Config", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox51.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer41.Add( self.m_checkBox51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer3.Add( bSizer41, 0, 0, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Working Folder:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.m_staticText5.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer6.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.txt_workingFolder = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CHARWRAP|wx.TE_READONLY|wx.NO_BORDER )
		self.txt_workingFolder.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.txt_workingFolder.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer6.Add( self.txt_workingFolder, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer3.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		self.m_dirPicker3 = wx.DirPickerCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		self.m_dirPicker3.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer3.Add( self.m_dirPicker3, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline3 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Saving Images:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 11, 72, 90, 92, False, "Cambria" ) )
		self.m_staticText6.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer3.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Image Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		self.m_staticText9.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer13.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textImageSaveTarget = wx.TextCtrl( self.m_panel2, wx.ID_ANY, u"(file name)", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.m_textImageSaveTarget.SetToolTipString( u"file is saved in the working directory above automatically" )
		self.m_textImageSaveTarget.SetMaxSize( wx.Size( 300,-1 ) )
		
		bSizer13.Add( self.m_textImageSaveTarget, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button1 = wx.Button( self.m_panel2, wx.ID_ANY, u"Save PNG", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.m_button1, 0, wx.ALL, 5 )
		
		self.m_button44 = wx.Button( self.m_panel2, wx.ID_ANY, u"Save SVG", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.m_button44, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer7.Add( bSizer13, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		self.m_staticline16 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline16, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer48 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer53 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer562 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button27 = wx.Button( self.m_panel2, wx.ID_ANY, u"Draw Cairo", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer562.Add( self.m_button27, 0, wx.ALL, 5 )
		
		
		bSizer562.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button461 = wx.Button( self.m_panel2, wx.ID_ANY, u"Save PNG, SVG and SEPP Legend", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer562.Add( self.m_button461, 0, wx.ALL, 5 )
		
		
		bSizer53.Add( bSizer562, 1, wx.EXPAND, 5 )
		
		
		bSizer48.Add( bSizer53, 1, wx.EXPAND, 5 )
		
		self.m_staticline191 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer48.Add( self.m_staticline191, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer57 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText61 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Write Image as SVG File:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		self.m_staticText61.SetFont( wx.Font( 11, 72, 90, 92, False, "Cambria" ) )
		self.m_staticText61.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer57.Add( self.m_staticText61, 0, wx.ALL, 5 )
		
		bSizer131 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText91 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"File Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )
		self.m_staticText91.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer131.Add( self.m_staticText91, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textSvgSaveTarget = wx.TextCtrl( self.m_panel2, wx.ID_ANY, u"(file name)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textSvgSaveTarget.SetToolTipString( u"file is saved in the working directory above automatically" )
		self.m_textSvgSaveTarget.SetMaxSize( wx.Size( 300,-1 ) )
		
		bSizer131.Add( self.m_textSvgSaveTarget, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button11 = wx.Button( self.m_panel2, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer131.Add( self.m_button11, 0, wx.ALL, 5 )
		
		
		bSizer57.Add( bSizer131, 0, wx.EXPAND, 5 )
		
		
		bSizer48.Add( bSizer57, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer48, 1, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer3 )
		self.m_panel2.Layout()
		bSizer3.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"Files", True )
		self.m_panel11 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel11.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		self.m_panel11.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		bSizer61 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFile = wx.StaticText( self.m_panel11, wx.ID_ANY, u"Tree File", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lblFile.Wrap( -1 )
		self.lblFile.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.lblFile.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer4.Add( self.lblFile, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_FilePicker_tree = wx.FilePickerCtrl( self.m_panel11, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 500,-1 ), wx.FLP_DEFAULT_STYLE )
		self.m_FilePicker_tree.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		bSizer4.Add( self.m_FilePicker_tree, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.btn_import_tree = wx.Button( self.m_panel11, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.btn_import_tree, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button372 = wx.Button( self.m_panel11, wx.ID_ANY, u"Export (Nwk)", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_button372, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer61.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		bSizer62 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer631 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer65 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox8 = wx.CheckBox( self.m_panel11, wx.ID_ANY, u"Unit Edge Lngths", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox8.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer65.Add( self.m_checkBox8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button431 = wx.Button( self.m_panel11, wx.ID_ANY, u"Fix Missing Edge Lengths", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer65.Add( self.m_button431, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer631.Add( bSizer65, 0, wx.EXPAND, 5 )
		
		
		bSizer62.Add( bSizer631, 1, wx.EXPAND, 5 )
		
		self.m_staticline21 = wx.StaticLine( self.m_panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer62.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer64 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_propertyGridManager1 = pg.PropertyGridManager(self.m_panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PGMAN_DEFAULT_STYLE)
		self.m_propertyGridManager1.SetExtraStyle( wx.propgrid.PG_EX_MODE_BUTTONS ) 
		
		self.m_propertyGridPage1 = self.m_propertyGridManager1.AddPage( u"Page", wx.NullBitmap );
		self.m_propertyGridItem1 = self.m_propertyGridPage1.Append( pg.StringProperty( u"File", u"File" ) ) 
		self.m_propertyGridItem2 = self.m_propertyGridPage1.Append( pg.IntProperty( u"# Taxa", u"# Taxa" ) ) 
		self.m_propertyGridItem3 = self.m_propertyGridPage1.Append( pg.FloatProperty( u"X min", u"X min" ) ) 
		self.m_propertyGridItem4 = self.m_propertyGridPage1.Append( pg.FloatProperty( u"X max", u"X max" ) ) 
		self.m_propertyGridItem5 = self.m_propertyGridPage1.Append( pg.FloatProperty( u"Y min", u"Y min" ) ) 
		self.m_propertyGridItem6 = self.m_propertyGridPage1.Append( pg.FloatProperty( u"Y max", u"Y max" ) ) 
		bSizer64.Add( self.m_propertyGridManager1, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer62.Add( bSizer64, 1, wx.EXPAND, 5 )
		
		
		bSizer61.Add( bSizer62, 1, wx.EXPAND, 5 )
		
		
		self.m_panel11.SetSizer( bSizer61 )
		self.m_panel11.Layout()
		bSizer61.Fit( self.m_panel11 )
		self.m_notebook1.AddPage( self.m_panel11, u"Tree", False )
		self.viewer_panel = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.FULL_REPAINT_ON_RESIZE|wx.TAB_TRAVERSAL )
		bSizer27 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel81 = wx.Panel( self.viewer_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel81.SetForegroundColour( wx.Colour( 255, 219, 183 ) )
		self.m_panel81.SetBackgroundColour( wx.Colour( 255, 219, 183 ) )
		
		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText22 = wx.StaticText( self.m_panel81, wx.ID_ANY, u"Zoom", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		self.m_staticText22.SetFont( wx.Font( 10, 74, 90, 92, False, "Arial" ) )
		self.m_staticText22.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer28.Add( self.m_staticText22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinBtn2 = wx.SpinButton( self.m_panel81, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_spinBtn2.SetMinSize( wx.Size( -1,20 ) )
		
		bSizer28.Add( self.m_spinBtn2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl10 = wx.TextCtrl( self.m_panel81, wx.ID_ANY, u"1.00", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_RIGHT )
		self.m_textCtrl10.SetMaxLength( 5 ) 
		bSizer28.Add( self.m_textCtrl10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer28.AddSpacer( ( 10, 0), 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticline10 = wx.StaticLine( self.m_panel81, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL|wx.LI_VERTICAL )
		bSizer28.Add( self.m_staticline10, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer28.AddSpacer( ( 10, 0), 0, 0, 5 )
		
		self.m_staticText221 = wx.StaticText( self.m_panel81, wx.ID_ANY, u"Rotation", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText221.Wrap( -1 )
		self.m_staticText221.SetFont( wx.Font( 10, 74, 90, 92, False, "Arial" ) )
		self.m_staticText221.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer28.Add( self.m_staticText221, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinBtn21 = wx.SpinButton( self.m_panel81, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_spinBtn21.SetMinSize( wx.Size( -1,20 ) )
		
		bSizer28.Add( self.m_spinBtn21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl101 = wx.TextCtrl( self.m_panel81, wx.ID_ANY, u"0", wx.DefaultPosition, wx.Size( 40,-1 ), wx.TE_PROCESS_ENTER|wx.TE_RIGHT )
		self.m_textCtrl101.SetMaxLength( 4 ) 
		bSizer28.Add( self.m_textCtrl101, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText26 = wx.StaticText( self.m_panel81, wx.ID_ANY, u"(deg)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		self.m_staticText26.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer28.Add( self.m_staticText26, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button10 = wx.Button( self.m_panel81, wx.ID_ANY, u"Redraw", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.m_button10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_wxPanelBackgroundColor = wx.ColourPickerCtrl( self.m_panel81, wx.ID_ANY, wx.Colour( 255, 255, 255 ), wx.DefaultPosition, wx.Size( 80,-1 ), wx.CLRP_DEFAULT_STYLE )
		bSizer28.Add( self.m_wxPanelBackgroundColor, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		self.m_panel81.SetSizer( bSizer28 )
		self.m_panel81.Layout()
		bSizer28.Fit( self.m_panel81 )
		bSizer27.Add( self.m_panel81, 0, wx.ALL|wx.EXPAND, 0 )
		
		
		self.viewer_panel.SetSizer( bSizer27 )
		self.viewer_panel.Layout()
		bSizer27.Fit( self.viewer_panel )
		self.m_notebook1.AddPage( self.viewer_panel, u"Viewer", False )
		self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetBackgroundColour( wx.Colour( 200, 200, 200 ) )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Annotation Properties", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 14, 71, 93, 90, True, "Bauhaus 93" ) )
		
		bSizer11.Add( self.m_staticText7, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFile1 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Taxon Metadata File", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lblFile1.Wrap( -1 )
		self.lblFile1.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.lblFile1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer5.Add( self.lblFile1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		self.m_FilePicker_annotation = wx.FilePickerCtrl( self.m_panel4, wx.ID_ANY, u"C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\kra-primate-project\\kra-primate\\tree_placement_2\\annotation.txt", u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		self.m_FilePicker_annotation.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer11.Add( self.m_FilePicker_annotation, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.btn_import_annotation = wx.Button( self.m_panel4, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.btn_import_annotation, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		self.m_staticline6 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer121 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText71 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Field to Annotate", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )
		bSizer121.Add( self.m_staticText71, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_ComboSelectedFieldChoices = []
		self.m_ComboSelectedField = wx.ComboBox( self.m_panel4, wx.ID_ANY, u"(select)", wx.DefaultPosition, wx.DefaultSize, m_ComboSelectedFieldChoices, 0 )
		bSizer121.Add( self.m_ComboSelectedField, 1, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer121, 0, wx.EXPAND, 5 )
		
		gbSizer11 = wx.GridBagSizer( 0, 0 )
		gbSizer11.SetFlexibleDirection( wx.BOTH )
		gbSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText411 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText411.Wrap( -1 )
		gbSizer11.Add( self.m_staticText411, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_comboBox51Choices = []
		self.m_comboBox51 = wx.ComboBox( self.m_panel4, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_comboBox51Choices, 0 )
		gbSizer11.Add( self.m_comboBox51, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_listBox31Choices = []
		self.m_listBox31 = wx.ListBox( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.Size( 230,-1 ), m_listBox31Choices, wx.LB_EXTENDED|wx.LB_NEEDED_SB|wx.LB_SORT )
		gbSizer11.Add( self.m_listBox31, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_listBox21Choices = [ u"option 1", u"option 2" ]
		self.m_listBox21 = wx.ListBox( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.Size( 230,-1 ), m_listBox21Choices, wx.LB_EXTENDED|wx.LB_SORT )
		gbSizer11.Add( self.m_listBox21, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )
		
		m_comboBox61Choices = []
		self.m_comboBox61 = wx.ComboBox( self.m_panel4, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_comboBox61Choices, 0 )
		gbSizer11.Add( self.m_comboBox61, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		gbSizer11.AddGrowableCol( 2 )
		
		bSizer11.Add( gbSizer11, 1, wx.EXPAND, 5 )
		
		self.m_staticline5 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer1211 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText711 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Circle Size (px)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText711.Wrap( -1 )
		bSizer1211.Add( self.m_staticText711, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl24 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 50,-1 ), wx.TE_PROCESS_ENTER )
		bSizer1211.Add( self.m_textCtrl24, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button4 = wx.Button( self.m_panel4, wx.ID_ANY, u"Trigger Redraw", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1211.Add( self.m_button4, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer1211, 0, wx.EXPAND, 5 )
		
		self.m_staticline51 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline51, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer42 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox4 = wx.CheckBox( self.m_panel4, wx.ID_ANY, u"Show Legend", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer42.Add( self.m_checkBox4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText34 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"W: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )
		bSizer42.Add( self.m_staticText34, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.m_textCtrl12 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,-1 ), wx.TE_PROCESS_ENTER|wx.TE_RIGHT )
		bSizer42.Add( self.m_textCtrl12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText341 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"H: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText341.Wrap( -1 )
		bSizer42.Add( self.m_staticText341, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
		
		self.m_textCtrl13 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,-1 ), wx.TE_PROCESS_ENTER|wx.TE_RIGHT )
		bSizer42.Add( self.m_textCtrl13, 0, wx.ALL, 5 )
		
		m_comboBox7Choices = [ u"Percentile", u"Value" ]
		self.m_comboBox7 = wx.ComboBox( self.m_panel4, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_comboBox7Choices, 0 )
		bSizer42.Add( self.m_comboBox7, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer42, 0, wx.EXPAND, 5 )
		
		bSizer561 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTextLegendFont = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Legend Font:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextLegendFont.Wrap( -1 )
		bSizer561.Add( self.m_staticTextLegendFont, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_fontPickerLegend = wx.FontPickerCtrl( self.m_panel4, wx.ID_ANY, wx.Font( 14, 70, 90, 90, False, "Cambria" ), wx.DefaultPosition, wx.DefaultSize, wx.FNTP_DEFAULT_STYLE )
		self.m_fontPickerLegend.SetMaxPointSize( 100 ) 
		bSizer561.Add( self.m_fontPickerLegend, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button26 = wx.Button( self.m_panel4, wx.ID_ANY, u"Internals", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer561.Add( self.m_button26, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_button34 = wx.Button( self.m_panel4, wx.ID_ANY, u"Leafs", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer561.Add( self.m_button34, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer561, 0, wx.EXPAND, 5 )
		
		bSizer63 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText50 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Legend Block Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText50.Wrap( -1 )
		bSizer63.Add( self.m_staticText50, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textLegendBlock = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.TE_PROCESS_ENTER )
		bSizer63.Add( self.m_textLegendBlock, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText51 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Legend Spacing", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText51.Wrap( -1 )
		bSizer63.Add( self.m_staticText51, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textLegendSpacing = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), wx.TE_PROCESS_ENTER )
		bSizer63.Add( self.m_textLegendSpacing, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer63, 0, wx.EXPAND, 5 )
		
		self.m_staticline201 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline201, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer60 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBoxShowRoot = wx.CheckBox( self.m_panel4, wx.ID_ANY, u"Show Root", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxShowRoot.SetValue(True) 
		bSizer60.Add( self.m_checkBoxShowRoot, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( bSizer60, 0, wx.EXPAND, 5 )
		
		
		bSizer11.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer10.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText8 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Values", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( 11, 72, 90, 92, False, "Cambria" ) )
		
		bSizer17.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button7 = wx.Button( self.m_panel4, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer17.Add( self.m_button7, 0, wx.ALL, 5 )
		
		self.m_button8 = wx.Button( self.m_panel4, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer17.Add( self.m_button8, 0, wx.ALL, 5 )
		
		self.m_button411 = wx.Button( self.m_panel4, wx.ID_ANY, u"Select All", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_button411, 0, wx.ALL, 5 )
		
		self.m_button421 = wx.Button( self.m_panel4, wx.ID_ANY, u"Unselect All", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_button421, 0, wx.ALL, 5 )
		
		
		bSizer12.Add( bSizer17, 0, 0, 5 )
		
		self.m_panel5 = wx.Panel( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_panel5.SetBackgroundColour( wx.Colour( 232, 238, 244 ) )
		
		bSizer29 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panel5.SetSizer( bSizer29 )
		self.m_panel5.Layout()
		bSizer29.Fit( self.m_panel5 )
		bSizer12.Add( self.m_panel5, 1, wx.ALL|wx.EXPAND, 1 )
		
		
		bSizer10.Add( bSizer12, 3, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer10 )
		self.m_panel4.Layout()
		bSizer10.Fit( self.m_panel4 )
		self.m_notebook1.AddPage( self.m_panel4, u"Taxon Annotation", False )
		self.m_panel41 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel41.SetBackgroundColour( wx.Colour( 200, 200, 200 ) )
		
		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer111 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText72 = wx.StaticText( self.m_panel41, wx.ID_ANY, u"SEPP Annotation Properties", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText72.Wrap( -1 )
		self.m_staticText72.SetFont( wx.Font( 14, 71, 93, 90, True, "Bauhaus 93" ) )
		
		bSizer111.Add( self.m_staticText72, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline19 = wx.StaticLine( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer111.Add( self.m_staticline19, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer511 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFile111 = wx.StaticText( self.m_panel41, wx.ID_ANY, u"SEPP Placement JSON", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lblFile111.Wrap( -1 )
		self.lblFile111.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.lblFile111.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer511.Add( self.lblFile111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer111.Add( bSizer511, 0, wx.EXPAND, 5 )
		
		self.m_filePicker5 = wx.FilePickerCtrl( self.m_panel41, wx.ID_ANY, u"C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\kra-primate-project\\kra-primate\\tree_placement_2\\place_repset_placement.json", u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer111.Add( self.m_filePicker5, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline20 = wx.StaticLine( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer111.Add( self.m_staticline20, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFile11 = wx.StaticText( self.m_panel41, wx.ID_ANY, u"SEPP Placement Metadata File", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lblFile11.Wrap( -1 )
		self.lblFile11.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.lblFile11.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer51.Add( self.lblFile11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer111.Add( bSizer51, 0, wx.EXPAND, 5 )
		
		self.m_FilePicker_annotation1 = wx.FilePickerCtrl( self.m_panel41, wx.ID_ANY, u"C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\kra-primate-project\\kra-primate\\tree_placement_2\\sepp_annotation.txt", u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		self.m_FilePicker_annotation1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer111.Add( self.m_FilePicker_annotation1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.btn_import_annotation1 = wx.Button( self.m_panel41, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer111.Add( self.btn_import_annotation1, 0, wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, 5 )
		
		self.m_staticline61 = wx.StaticLine( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer111.Add( self.m_staticline61, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer1212 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText712 = wx.StaticText( self.m_panel41, wx.ID_ANY, u"Field to Annotate", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText712.Wrap( -1 )
		bSizer1212.Add( self.m_staticText712, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_ComboSelectedField1Choices = []
		self.m_ComboSelectedField1 = wx.ComboBox( self.m_panel41, wx.ID_ANY, u"(select)", wx.DefaultPosition, wx.DefaultSize, m_ComboSelectedField1Choices, 0 )
		bSizer1212.Add( self.m_ComboSelectedField1, 1, wx.ALL, 5 )
		
		
		bSizer111.Add( bSizer1212, 0, wx.EXPAND, 5 )
		
		bSizer43 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox5 = wx.CheckBox( self.m_panel41, wx.ID_ANY, u"Import as Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer43.Add( self.m_checkBox5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button17 = wx.Button( self.m_panel41, wx.ID_ANY, u"Draw Circles", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer43.Add( self.m_button17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button18 = wx.Button( self.m_panel41, wx.ID_ANY, u"Clear Circles", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer43.Add( self.m_button18, 0, wx.ALL, 5 )
		
		
		bSizer111.Add( bSizer43, 0, wx.EXPAND, 5 )
		
		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText41 = wx.StaticText( self.m_panel41, wx.ID_ANY, u"Filters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		gbSizer1.Add( self.m_staticText41, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_comboBox5Choices = []
		self.m_comboBox5 = wx.ComboBox( self.m_panel41, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_comboBox5Choices, 0 )
		gbSizer1.Add( self.m_comboBox5, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_listBox3Choices = []
		self.m_listBox3 = wx.ListBox( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.Size( 230,-1 ), m_listBox3Choices, wx.LB_EXTENDED|wx.LB_NEEDED_SB|wx.LB_SORT )
		gbSizer1.Add( self.m_listBox3, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		m_listBox2Choices = []
		self.m_listBox2 = wx.ListBox( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.Size( 230,-1 ), m_listBox2Choices, wx.LB_EXTENDED|wx.LB_SORT )
		gbSizer1.Add( self.m_listBox2, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )
		
		m_comboBox6Choices = []
		self.m_comboBox6 = wx.ComboBox( self.m_panel41, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize, m_comboBox6Choices, 0 )
		gbSizer1.Add( self.m_comboBox6, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
		
		
		gbSizer1.AddGrowableCol( 2 )
		
		bSizer111.Add( gbSizer1, 1, wx.EXPAND, 5 )
		
		self.m_staticline52 = wx.StaticLine( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer111.Add( self.m_staticline52, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer12111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText7111 = wx.StaticText( self.m_panel41, wx.ID_ANY, u"Circle Props: Size (px)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7111.Wrap( -1 )
		bSizer12111.Add( self.m_staticText7111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl25 = wx.TextCtrl( self.m_panel41, wx.ID_ANY, u"25", wx.DefaultPosition, wx.Size( 50,-1 ), wx.TE_PROCESS_ENTER )
		bSizer12111.Add( self.m_textCtrl25, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button41 = wx.Button( self.m_panel41, wx.ID_ANY, u"Trigger Redraw", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12111.Add( self.m_button41, 0, wx.ALL, 5 )
		
		self.m_colourPicker2 = wx.ColourPickerCtrl( self.m_panel41, wx.ID_ANY, wx.Colour( 255, 0, 0 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer12111.Add( self.m_colourPicker2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer111.Add( bSizer12111, 0, wx.EXPAND, 5 )
		
		self.m_staticline511 = wx.StaticLine( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer111.Add( self.m_staticline511, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer66 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer67 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBox3 = wx.CheckBox( self.m_panel41, wx.ID_ANY, u"Draw with Pendant Branch", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer67.Add( self.m_checkBox3, 0, wx.ALL, 5 )
		
		self.m_checkBox6 = wx.CheckBox( self.m_panel41, wx.ID_ANY, u"Jitter Attachment Point", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox6.SetValue(True) 
		bSizer67.Add( self.m_checkBox6, 0, wx.ALL, 5 )
		
		self.m_checkSeppShowAll = wx.CheckBox( self.m_panel41, wx.ID_ANY, u"Show All Placement Locations (alt: show top 1)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkSeppShowAll.SetValue(True) 
		bSizer67.Add( self.m_checkSeppShowAll, 0, wx.ALL, 5 )
		
		
		bSizer66.Add( bSizer67, 0, 0, 0 )
		
		bSizer68 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button441 = wx.Button( self.m_panel41, wx.ID_ANY, u"6-color", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer68.Add( self.m_button441, 0, wx.ALL, 5 )
		
		self.m_saveSeppLegend = wx.Button( self.m_panel41, wx.ID_ANY, u"Save Legend", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer68.Add( self.m_saveSeppLegend, 0, wx.ALL, 5 )
		
		
		bSizer66.Add( bSizer68, 1, wx.EXPAND, 5 )
		
		
		bSizer111.Add( bSizer66, 0, wx.ALIGN_CENTER_HORIZONTAL, 0 )
		
		self.m_staticline71 = wx.StaticLine( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer111.Add( self.m_staticline71, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer111.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer101.Add( bSizer111, 1, wx.EXPAND, 5 )
		
		bSizer122 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer171 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText81 = wx.StaticText( self.m_panel41, wx.ID_ANY, u"Values", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )
		self.m_staticText81.SetFont( wx.Font( 11, 72, 90, 92, False, "Cambria" ) )
		
		bSizer171.Add( self.m_staticText81, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button71 = wx.Button( self.m_panel41, wx.ID_ANY, u"Clear Values", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_button71, 0, wx.ALL, 5 )
		
		self.m_button81 = wx.Button( self.m_panel41, wx.ID_ANY, u"Load Values", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_button81, 0, wx.ALL, 5 )
		
		self.m_button42 = wx.Button( self.m_panel41, wx.ID_ANY, u"Select All", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_button42, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button43 = wx.Button( self.m_panel41, wx.ID_ANY, u"Unselect All", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer171.Add( self.m_button43, 0, wx.ALL, 5 )
		
		
		bSizer122.Add( bSizer171, 0, 0, 5 )
		
		self.m_panel51 = wx.Panel( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel51.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_panel51.SetBackgroundColour( wx.Colour( 223, 253, 228 ) )
		
		bSizer291 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panel51.SetSizer( bSizer291 )
		self.m_panel51.Layout()
		bSizer291.Fit( self.m_panel51 )
		bSizer122.Add( self.m_panel51, 1, wx.ALL|wx.EXPAND, 1 )
		
		
		bSizer101.Add( bSizer122, 3, wx.EXPAND, 5 )
		
		
		self.m_panel41.SetSizer( bSizer101 )
		self.m_panel41.Layout()
		bSizer101.Fit( self.m_panel41 )
		self.m_notebook1.AddPage( self.m_panel41, u"SEPP Annotation", False )
		self.m_ExtraAnnotation = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer512 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_grid1 = wx.grid.Grid( self.m_ExtraAnnotation, wx.ID_ANY, wx.DefaultPosition, wx.Size( 320,-1 ), 0 )
		
		# Grid
		self.m_grid1.CreateGrid( 30, 3 )
		self.m_grid1.EnableEditing( False )
		self.m_grid1.EnableGridLines( True )
		self.m_grid1.EnableDragGridSize( False )
		self.m_grid1.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid1.SetColSize( 0, 100 )
		self.m_grid1.SetColSize( 1, 100 )
		self.m_grid1.SetColSize( 2, 100 )
		self.m_grid1.EnableDragColMove( False )
		self.m_grid1.EnableDragColSize( True )
		self.m_grid1.SetColLabelSize( 30 )
		self.m_grid1.SetColLabelValue( 0, u"Type" )
		self.m_grid1.SetColLabelValue( 1, u"Point" )
		self.m_grid1.SetColLabelValue( 2, u"Name" )
		self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.m_grid1.EnableDragRowSize( True )
		self.m_grid1.SetRowLabelSize( 0 )
		self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer512.Add( self.m_grid1, 1, wx.ALL, 5 )
		
		
		self.m_ExtraAnnotation.SetSizer( bSizer512 )
		self.m_ExtraAnnotation.Layout()
		bSizer512.Fit( self.m_ExtraAnnotation )
		self.m_notebook1.AddPage( self.m_ExtraAnnotation, u"Extra Annotation", False )
		self.m_panel8 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button5 = wx.Button( self.m_panel8, wx.ID_ANY, u"Run Controller Script", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.m_button5, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( bSizer16, 0, wx.EXPAND, 5 )
		
		self.m_staticline18 = wx.StaticLine( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer15.Add( self.m_staticline18, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer54 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button28 = wx.Button( self.m_panel8, wx.ID_ANY, u"Test 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer54.Add( self.m_button28, 0, wx.ALL, 5 )
		
		self.m_button29 = wx.Button( self.m_panel8, wx.ID_ANY, u"Test 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer54.Add( self.m_button29, 0, wx.ALL, 5 )
		
		self.m_button30 = wx.Button( self.m_panel8, wx.ID_ANY, u"Test 3", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer54.Add( self.m_button30, 0, wx.ALL, 5 )
		
		self.m_button31 = wx.Button( self.m_panel8, wx.ID_ANY, u"Test 4", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer54.Add( self.m_button31, 0, wx.ALL, 5 )
		
		
		bSizer15.Add( bSizer54, 1, wx.EXPAND, 5 )
		
		
		self.m_panel8.SetSizer( bSizer15 )
		self.m_panel8.Layout()
		bSizer15.Fit( self.m_panel8 )
		self.m_notebook1.AddPage( self.m_panel8, u"Console", False )
		self.m_panel82 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel82.SetBackgroundColour( wx.Colour( 251, 209, 191 ) )
		
		bSizer151 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer89 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer91 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText74 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Tree Line Width", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		self.m_staticText74.Wrap( -1 )
		bSizer91.Add( self.m_staticText74, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textTreeLineWidth = wx.TextCtrl( self.m_panel82, wx.ID_ANY, u".004", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		bSizer91.Add( self.m_textTreeLineWidth, 0, wx.ALL, 5 )
		
		
		bSizer89.Add( bSizer91, 0, 0, 5 )
		
		bSizer911 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText741 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Tree Line Color", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		self.m_staticText741.Wrap( -1 )
		bSizer911.Add( self.m_staticText741, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_treeLineColor = wx.ColourPickerCtrl( self.m_panel82, wx.ID_ANY, wx.Colour( 128, 128, 128 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer911.Add( self.m_treeLineColor, 0, wx.ALL, 5 )
		
		self.m_staticline22 = wx.StaticLine( self.m_panel82, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer911.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText47 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Img Background", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )
		bSizer911.Add( self.m_staticText47, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_cairoBackgroundColor = wx.ColourPickerCtrl( self.m_panel82, wx.ID_ANY, wx.Colour( 240, 240, 240 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer911.Add( self.m_cairoBackgroundColor, 0, wx.ALL, 5 )
		
		
		bSizer89.Add( bSizer911, 0, 0, 5 )
		
		self.m_staticline161 = wx.StaticLine( self.m_panel82, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer89.Add( self.m_staticline161, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer9711 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText7812 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"PNG Width", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7812.Wrap( -1 )
		self.m_staticText7812.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer9711.Add( self.m_staticText7812, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textPngWidth = wx.TextCtrl( self.m_panel82, wx.ID_ANY, u"1500", wx.DefaultPosition, wx.Size( 75,-1 ), wx.TE_PROCESS_ENTER )
		bSizer9711.Add( self.m_textPngWidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer9711.AddSpacer( ( 20, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText78111 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Height", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText78111.Wrap( -1 )
		self.m_staticText78111.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer9711.Add( self.m_staticText78111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textPngHeight = wx.TextCtrl( self.m_panel82, wx.ID_ANY, u"900", wx.DefaultPosition, wx.Size( 75,-1 ), wx.TE_PROCESS_ENTER )
		bSizer9711.Add( self.m_textPngHeight, 0, wx.ALL, 5 )
		
		
		bSizer89.Add( bSizer9711, 0, 0, 5 )
		
		bSizer97111 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_textCircleAlphas = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Circle Alphas", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCircleAlphas.Wrap( -1 )
		self.m_textCircleAlphas.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer97111.Add( self.m_textCircleAlphas, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCircleAlphas = wx.TextCtrl( self.m_panel82, wx.ID_ANY, u".75", wx.DefaultPosition, wx.Size( 75,-1 ), wx.TE_PROCESS_ENTER )
		bSizer97111.Add( self.m_textCircleAlphas, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer97111.AddSpacer( ( 20, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText781111 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"SEPP alphas", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText781111.Wrap( -1 )
		self.m_staticText781111.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer97111.Add( self.m_staticText781111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textSeppAlphas = wx.TextCtrl( self.m_panel82, wx.ID_ANY, u".45", wx.DefaultPosition, wx.Size( 75,-1 ), wx.TE_PROCESS_ENTER )
		bSizer97111.Add( self.m_textSeppAlphas, 0, wx.ALL, 5 )
		
		
		bSizer89.Add( bSizer97111, 0, 0, 5 )
		
		bSizer55 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button32 = wx.Button( self.m_panel82, wx.ID_ANY, u"Draw Cairo", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer55.Add( self.m_button32, 0, wx.ALL, 5 )
		
		self.m_stCairoDrawCount = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Draw Count: ", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_stCairoDrawCount.Wrap( -1 )
		bSizer55.Add( self.m_stCairoDrawCount, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button33 = wx.Button( self.m_panel82, wx.ID_ANY, u"Reload Tree Module", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer55.Add( self.m_button33, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer89.Add( bSizer55, 0, wx.EXPAND, 5 )
		
		
		bSizer151.Add( bSizer89, 1, wx.EXPAND, 5 )
		
		self.m_staticline32 = wx.StaticLine( self.m_panel82, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer151.Add( self.m_staticline32, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer90 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer92 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer96 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText77 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Tree Manipulator", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText77.Wrap( -1 )
		self.m_staticText77.SetFont( wx.Font( 12, 74, 90, 92, False, "Arial" ) )
		self.m_staticText77.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer96.Add( self.m_staticText77, 0, wx.ALL, 5 )
		
		bSizer97 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText78 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Active Edge:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText78.Wrap( -1 )
		self.m_staticText78.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer97.Add( self.m_staticText78, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl33 = wx.TextCtrl( self.m_panel82, wx.ID_ANY, u"None", wx.DefaultPosition, wx.Size( 200,-1 ), wx.TE_READONLY|wx.NO_BORDER )
		bSizer97.Add( self.m_textCtrl33, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button36 = wx.Button( self.m_panel82, wx.ID_ANY, u"Reroot Above", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer97.Add( self.m_button36, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer96.Add( bSizer97, 0, 0, 5 )
		
		bSizer971 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText781 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Wedge Angle (w)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText781.Wrap( -1 )
		self.m_staticText781.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer971.Add( self.m_staticText781, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl331 = wx.TextCtrl( self.m_panel82, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		bSizer971.Add( self.m_textCtrl331, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer971.AddSpacer( ( 20, 0), 1, wx.EXPAND, 5 )
		
		self.m_staticText7811 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Right Border (t):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7811.Wrap( -1 )
		self.m_staticText7811.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer971.Add( self.m_staticText7811, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl3311 = wx.TextCtrl( self.m_panel82, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 75,-1 ), 0 )
		bSizer971.Add( self.m_textCtrl3311, 0, wx.ALL, 5 )
		
		
		bSizer96.Add( bSizer971, 0, 0, 5 )
		
		bSizer98 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText79 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Pivot Branch:", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText79.Wrap( -1 )
		self.m_staticText79.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer98.Add( self.m_staticText79, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button37 = wx.Button( self.m_panel82, wx.ID_ANY, u"Clockwise", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer98.Add( self.m_button37, 0, wx.ALL, 5 )
		
		self.m_button38 = wx.Button( self.m_panel82, wx.ID_ANY, u"Counterclockwise", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer98.Add( self.m_button38, 0, wx.ALL, 5 )
		
		
		bSizer96.Add( bSizer98, 0, 0, 5 )
		
		bSizer981 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText791 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"Expand Branch:", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_staticText791.Wrap( -1 )
		self.m_staticText791.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer981.Add( self.m_staticText791, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button371 = wx.Button( self.m_panel82, wx.ID_ANY, u"Out", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer981.Add( self.m_button371, 0, wx.ALL, 5 )
		
		self.m_button381 = wx.Button( self.m_panel82, wx.ID_ANY, u"In", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer981.Add( self.m_button381, 0, wx.ALL, 5 )
		
		
		bSizer96.Add( bSizer981, 0, 0, 5 )
		
		bSizer99 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button45 = wx.Button( self.m_panel82, wx.ID_ANY, u"Redraw Tree", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer99.Add( self.m_button45, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer107 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button46 = wx.Button( self.m_panel82, wx.ID_ANY, u"Save RP File", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer107.Add( self.m_button46, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_dirPicker4 = wx.DirPickerCtrl( self.m_panel82, wx.ID_ANY, u"C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\phylostrator-testing\\rdp_images", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer107.Add( self.m_dirPicker4, 1, wx.ALL, 5 )
		
		
		bSizer99.Add( bSizer107, 0, wx.EXPAND, 5 )
		
		bSizer56 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText43 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"File Name", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText43.Wrap( -1 )
		bSizer56.Add( self.m_staticText43, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer56.AddSpacer( ( 25, 0), 0, 0, 5 )
		
		self.m_textCtrl17 = wx.TextCtrl( self.m_panel82, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer56.Add( self.m_textCtrl17, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer99.Add( bSizer56, 0, wx.EXPAND, 5 )
		
		self.m_staticline17 = wx.StaticLine( self.m_panel82, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer99.Add( self.m_staticline17, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer52 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button25 = wx.Button( self.m_panel82, wx.ID_ANY, u"Fill Space", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer52.Add( self.m_button25, 0, wx.ALL, 5 )
		
		self.m_button35 = wx.Button( self.m_panel82, wx.ID_ANY, u"Save Cairo Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer52.Add( self.m_button35, 0, wx.ALL, 5 )
		
		
		bSizer99.Add( bSizer52, 0, 0, 5 )
		
		self.m_staticText40 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		bSizer99.Add( self.m_staticText40, 0, wx.ALL, 5 )
		
		self.m_staticText412 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText412.Wrap( -1 )
		bSizer99.Add( self.m_staticText412, 0, wx.ALL, 5 )
		
		self.m_staticText42 = wx.StaticText( self.m_panel82, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		bSizer99.Add( self.m_staticText42, 0, wx.ALL, 5 )
		
		
		bSizer96.Add( bSizer99, 1, wx.EXPAND, 5 )
		
		
		bSizer92.Add( bSizer96, 1, wx.EXPAND, 5 )
		
		
		bSizer90.Add( bSizer92, 1, wx.EXPAND, 5 )
		
		
		bSizer151.Add( bSizer90, 1, wx.EXPAND, 5 )
		
		
		self.m_panel82.SetSizer( bSizer151 )
		self.m_panel82.Layout()
		bSizer151.Fit( self.m_panel82 )
		self.m_notebook1.AddPage( self.m_panel82, u"Cairo", False )
		
		bSizer2.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_frame_close )
		self.Bind( wx.EVT_ICONIZE, self.on_frame_iconize )
		self.m_FilePicker_config.Bind( wx.EVT_FILEPICKER_CHANGED, self.set_file )
		self.btn_import_tree1.Bind( wx.EVT_BUTTON, self.import_tree )
		self.m_checkBox51.Bind( wx.EVT_CHECKBOX, self.on_toggle_config )
		self.m_dirPicker3.Bind( wx.EVT_DIRPICKER_CHANGED, self.set_working_folder )
		self.m_textImageSaveTarget.Bind( wx.EVT_TEXT, self.set_cairo_image_path )
		self.m_button1.Bind( wx.EVT_BUTTON, self.save_cairo_image )
		self.m_button44.Bind( wx.EVT_BUTTON, self.save_as_svg_from_png_filename )
		self.m_button27.Bind( wx.EVT_BUTTON, self.on_draw_cairo_click )
		self.m_button461.Bind( wx.EVT_BUTTON, self.on_save_sepp_legend_click )
		self.m_button11.Bind( wx.EVT_BUTTON, self.save_as_svg_click )
		self.m_FilePicker_tree.Bind( wx.EVT_FILEPICKER_CHANGED, self.set_file )
		self.btn_import_tree.Bind( wx.EVT_BUTTON, self.import_tree )
		self.m_button372.Bind( wx.EVT_BUTTON, self.save_tree_as_newick )
		self.m_button431.Bind( wx.EVT_BUTTON, self.on_fix_missing_edge_lengths_click )
		self.viewer_panel.Bind( wx.EVT_PAINT, self.on_zoompanel_holder_paint )
		self.m_spinBtn2.Bind( wx.EVT_SPIN_DOWN, self.zoom_out_10pct )
		self.m_spinBtn2.Bind( wx.EVT_SPIN_UP, self.zoom_in_10pct )
		self.m_textCtrl10.Bind( wx.EVT_TEXT, self.adjust_zoom )
		self.m_spinBtn21.Bind( wx.EVT_SPIN_DOWN, self.rotate_clockwise )
		self.m_spinBtn21.Bind( wx.EVT_SPIN_UP, self.rotate_counterclockwise )
		self.m_textCtrl101.Bind( wx.EVT_TEXT_ENTER, self.adjust_rotation )
		self.m_button10.Bind( wx.EVT_BUTTON, self.adjust_rotation )
		self.m_wxPanelBackgroundColor.Bind( wx.EVT_COLOURPICKER_CHANGED, self.on_wx_panel_background_changed )
		self.m_FilePicker_annotation.Bind( wx.EVT_FILEPICKER_CHANGED, self.set_annotation_file )
		self.btn_import_annotation.Bind( wx.EVT_BUTTON, self.import_annotation )
		self.m_ComboSelectedField.Bind( wx.EVT_COMBOBOX, self.populate_annotation_values )
		self.m_ComboSelectedField.Bind( wx.EVT_TEXT, self.populate_annotation_values )
		self.m_comboBox51.Bind( wx.EVT_COMBOBOX, self.load_filter1 )
		self.m_listBox31.Bind( wx.EVT_LISTBOX, self.process_filter1 )
		self.m_listBox21.Bind( wx.EVT_LISTBOX, self.process_filter2 )
		self.m_comboBox61.Bind( wx.EVT_COMBOBOX, self.load_filter2 )
		self.m_textCtrl24.Bind( wx.EVT_TEXT_ENTER, self.reset_all_circle_sizes )
		self.m_button4.Bind( wx.EVT_BUTTON, self.trigger_redraw )
		self.m_checkBox4.Bind( wx.EVT_CHECKBOX, self.on_show_legend_check )
		self.m_textCtrl12.Bind( wx.EVT_TEXT_ENTER, self.move_legend )
		self.m_textCtrl13.Bind( wx.EVT_TEXT_ENTER, self.move_legend )
		self.m_button26.Bind( wx.EVT_BUTTON, self.on_draw_internal_labels_click )
		self.m_button34.Bind( wx.EVT_BUTTON, self.on_draw_leaf_labels )
		self.m_textLegendBlock.Bind( wx.EVT_TEXT_ENTER, self.populate_options_from_text_fields )
		self.m_textLegendSpacing.Bind( wx.EVT_TEXT_ENTER, self.populate_options_from_text_fields )
		self.m_checkBoxShowRoot.Bind( wx.EVT_CHECKBOX, self.on_show_root_check )
		self.m_button7.Bind( wx.EVT_BUTTON, self.valpicker_clear )
		self.m_button8.Bind( wx.EVT_BUTTON, self.valpicker_load )
		self.m_button411.Bind( wx.EVT_BUTTON, self.on_select_all_annotation_values )
		self.m_button421.Bind( wx.EVT_BUTTON, self.on_unselect_all_annotation_values )
		self.btn_import_annotation1.Bind( wx.EVT_BUTTON, self.sepp_import_annotation )
		self.m_ComboSelectedField1.Bind( wx.EVT_COMBOBOX, self.sepp_populate_annotation_values )
		self.m_ComboSelectedField1.Bind( wx.EVT_TEXT, self.sepp_populate_annotation_values )
		self.m_button17.Bind( wx.EVT_BUTTON, self.draw_circles )
		self.m_button18.Bind( wx.EVT_BUTTON, self.clear_extra_circles )
		self.m_comboBox5.Bind( wx.EVT_COMBOBOX, self.sepp_load_filter1 )
		self.m_listBox3.Bind( wx.EVT_LISTBOX, self.sepp_process_filter1 )
		self.m_listBox2.Bind( wx.EVT_LISTBOX, self.sepp_process_filter2 )
		self.m_comboBox6.Bind( wx.EVT_COMBOBOX, self.sepp_load_filter2 )
		self.m_textCtrl25.Bind( wx.EVT_TEXT_ENTER, self.sepp_set_uniform_size )
		self.m_button41.Bind( wx.EVT_BUTTON, self.trigger_redraw )
		self.m_colourPicker2.Bind( wx.EVT_COLOURPICKER_CHANGED, self.sepp_set_uniform_color )
		self.m_checkBox3.Bind( wx.EVT_CHECKBOX, self.set_pendant_branch_checked )
		self.m_checkSeppShowAll.Bind( wx.EVT_CHECKBOX, self.sepp_show_all_check )
		self.m_button441.Bind( wx.EVT_BUTTON, self.on_sepp_six_color )
		self.m_saveSeppLegend.Bind( wx.EVT_BUTTON, self.on_save_sepp_legend_click )
		self.m_button71.Bind( wx.EVT_BUTTON, self.sepp_valpicker_clear )
		self.m_button81.Bind( wx.EVT_BUTTON, self.sepp_valpicker_load )
		self.m_button42.Bind( wx.EVT_BUTTON, self.sepp_select_all )
		self.m_button43.Bind( wx.EVT_BUTTON, self.sepp_unselect_all )
		self.m_button5.Bind( wx.EVT_BUTTON, self.run_controller_script )
		self.m_button28.Bind( wx.EVT_BUTTON, self.on_test_1_click )
		self.m_button29.Bind( wx.EVT_BUTTON, self.on_test_2_click )
		self.m_button30.Bind( wx.EVT_BUTTON, self.on_test_3_click )
		self.m_button31.Bind( wx.EVT_BUTTON, self.on_test_4_click )
		self.m_textTreeLineWidth.Bind( wx.EVT_TEXT_ENTER, self.populate_options_from_text_fields )
		self.m_treeLineColor.Bind( wx.EVT_COLOURPICKER_CHANGED, self.on_tree_line_color_change )
		self.m_cairoBackgroundColor.Bind( wx.EVT_COLOURPICKER_CHANGED, self.on_cairo_background_change )
		self.m_textPngWidth.Bind( wx.EVT_TEXT_ENTER, self.populate_options_from_text_fields )
		self.m_textPngHeight.Bind( wx.EVT_TEXT_ENTER, self.populate_options_from_text_fields )
		self.m_textCircleAlphas.Bind( wx.EVT_TEXT_ENTER, self.populate_options_from_text_fields )
		self.m_textSeppAlphas.Bind( wx.EVT_TEXT_ENTER, self.populate_options_from_text_fields )
		self.m_button32.Bind( wx.EVT_BUTTON, self.on_draw_cairo_click )
		self.m_button33.Bind( wx.EVT_BUTTON, self.on_reload_tree_module )
		self.m_button36.Bind( wx.EVT_BUTTON, self.reroot_above )
		self.m_button37.Bind( wx.EVT_BUTTON, self.pivot_clock )
		self.m_button38.Bind( wx.EVT_BUTTON, self.pivot_ctrclock )
		self.m_button371.Bind( wx.EVT_BUTTON, self.expand_clade_out )
		self.m_button381.Bind( wx.EVT_BUTTON, self.expand_clade_in )
		self.m_button45.Bind( wx.EVT_BUTTON, self.redraw_tree )
		self.m_button46.Bind( wx.EVT_BUTTON, self.save_rp_file )
		self.m_button25.Bind( wx.EVT_BUTTON, self.on_fill_space_click )
		self.m_button35.Bind( wx.EVT_BUTTON, self.save_cairo_image )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_frame_close( self, event ):
		event.Skip()
	
	def on_frame_iconize( self, event ):
		event.Skip()
	
	def set_file( self, event ):
		event.Skip()
	
	def import_tree( self, event ):
		event.Skip()
	
	def on_toggle_config( self, event ):
		event.Skip()
	
	def set_working_folder( self, event ):
		event.Skip()
	
	def set_cairo_image_path( self, event ):
		event.Skip()
	
	def save_cairo_image( self, event ):
		event.Skip()
	
	def save_as_svg_from_png_filename( self, event ):
		event.Skip()
	
	def on_draw_cairo_click( self, event ):
		event.Skip()
	
	def on_save_sepp_legend_click( self, event ):
		event.Skip()
	
	def save_as_svg_click( self, event ):
		event.Skip()
	
	
	
	def save_tree_as_newick( self, event ):
		event.Skip()
	
	def on_fix_missing_edge_lengths_click( self, event ):
		event.Skip()
	
	def on_zoompanel_holder_paint( self, event ):
		event.Skip()
	
	def zoom_out_10pct( self, event ):
		event.Skip()
	
	def zoom_in_10pct( self, event ):
		event.Skip()
	
	def adjust_zoom( self, event ):
		event.Skip()
	
	def rotate_clockwise( self, event ):
		event.Skip()
	
	def rotate_counterclockwise( self, event ):
		event.Skip()
	
	def adjust_rotation( self, event ):
		event.Skip()
	
	
	def on_wx_panel_background_changed( self, event ):
		event.Skip()
	
	def set_annotation_file( self, event ):
		event.Skip()
	
	def import_annotation( self, event ):
		event.Skip()
	
	def populate_annotation_values( self, event ):
		event.Skip()
	
	
	def load_filter1( self, event ):
		event.Skip()
	
	def process_filter1( self, event ):
		event.Skip()
	
	def process_filter2( self, event ):
		event.Skip()
	
	def load_filter2( self, event ):
		event.Skip()
	
	def reset_all_circle_sizes( self, event ):
		event.Skip()
	
	def trigger_redraw( self, event ):
		event.Skip()
	
	def on_show_legend_check( self, event ):
		event.Skip()
	
	def move_legend( self, event ):
		event.Skip()
	
	
	def on_draw_internal_labels_click( self, event ):
		event.Skip()
	
	def on_draw_leaf_labels( self, event ):
		event.Skip()
	
	def populate_options_from_text_fields( self, event ):
		event.Skip()
	
	
	def on_show_root_check( self, event ):
		event.Skip()
	
	def valpicker_clear( self, event ):
		event.Skip()
	
	def valpicker_load( self, event ):
		event.Skip()
	
	def on_select_all_annotation_values( self, event ):
		event.Skip()
	
	def on_unselect_all_annotation_values( self, event ):
		event.Skip()
	
	def sepp_import_annotation( self, event ):
		event.Skip()
	
	def sepp_populate_annotation_values( self, event ):
		event.Skip()
	
	
	def draw_circles( self, event ):
		event.Skip()
	
	def clear_extra_circles( self, event ):
		event.Skip()
	
	def sepp_load_filter1( self, event ):
		event.Skip()
	
	def sepp_process_filter1( self, event ):
		event.Skip()
	
	def sepp_process_filter2( self, event ):
		event.Skip()
	
	def sepp_load_filter2( self, event ):
		event.Skip()
	
	def sepp_set_uniform_size( self, event ):
		event.Skip()
	
	
	def sepp_set_uniform_color( self, event ):
		event.Skip()
	
	def set_pendant_branch_checked( self, event ):
		event.Skip()
	
	def sepp_show_all_check( self, event ):
		event.Skip()
	
	def on_sepp_six_color( self, event ):
		event.Skip()
	
	
	def sepp_valpicker_clear( self, event ):
		event.Skip()
	
	def sepp_valpicker_load( self, event ):
		event.Skip()
	
	def sepp_select_all( self, event ):
		event.Skip()
	
	def sepp_unselect_all( self, event ):
		event.Skip()
	
	def run_controller_script( self, event ):
		event.Skip()
	
	def on_test_1_click( self, event ):
		event.Skip()
	
	def on_test_2_click( self, event ):
		event.Skip()
	
	def on_test_3_click( self, event ):
		event.Skip()
	
	def on_test_4_click( self, event ):
		event.Skip()
	
	
	def on_tree_line_color_change( self, event ):
		event.Skip()
	
	def on_cairo_background_change( self, event ):
		event.Skip()
	
	
	
	
	
	
	def on_reload_tree_module( self, event ):
		event.Skip()
	
	def reroot_above( self, event ):
		event.Skip()
	
	def pivot_clock( self, event ):
		event.Skip()
	
	def pivot_ctrclock( self, event ):
		event.Skip()
	
	def expand_clade_out( self, event ):
		event.Skip()
	
	def expand_clade_in( self, event ):
		event.Skip()
	
	def redraw_tree( self, event ):
		event.Skip()
	
	def save_rp_file( self, event ):
		event.Skip()
	
	def on_fill_space_click( self, event ):
		event.Skip()
	
	

###########################################################################
## Class AddTxtDialog
###########################################################################

class AddTxtDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 250,250 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer52 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText44 = wx.StaticText( self, wx.ID_ANY, u"Text Label:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )
		bSizer52.Add( self.m_staticText44, 0, wx.ALL, 5 )
		
		self.m_textCtrl13 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer52.Add( self.m_textCtrl13, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline21 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer52.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_fontPicker4 = wx.FontPickerCtrl( self, wx.ID_ANY, wx.Font( 11, 70, 90, 92, False, "Arial" ), wx.DefaultPosition, wx.DefaultSize, wx.FNTP_DEFAULT_STYLE )
		self.m_fontPicker4.SetMaxPointSize( 100 ) 
		bSizer52.Add( self.m_fontPicker4, 0, wx.ALL, 5 )
		
		
		bSizer52.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer53 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button22 = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer53.Add( self.m_button22, 1, wx.ALL, 5 )
		
		self.m_button23 = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer53.Add( self.m_button23, 1, wx.ALL, 5 )
		
		
		bSizer52.Add( bSizer53, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer52 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button22.Bind( wx.EVT_BUTTON, self.on_button_cancel )
		self.m_button23.Bind( wx.EVT_BUTTON, self.on_button_ok )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_button_cancel( self, event ):
		event.Skip()
	
	def on_button_ok( self, event ):
		event.Skip()
	

