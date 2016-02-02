# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

from view_classes import ViewAreaSelectorPanel
import wx
import wx.xrc

###########################################################################
## Class imgFrame
###########################################################################

class imgFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Phylostrator", pos = wx.DefaultPosition, size = wx.Size( 1058,759 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.img_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.FULL_REPAINT_ON_RESIZE|wx.TAB_TRAVERSAL )
		self.img_panel.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.img_panel.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		bSizer1.Add( self.img_panel, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar2 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.icnControlPanel = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"resources/icnControls30.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_CHECK, u"Control Panel", u"Show/Hide the Control Panel", None ) 
		
		self.m_toolBar1.Realize() 
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.img_panel.Bind( wx.EVT_PAINT, self.OnImgPaint )
		self.Bind( wx.EVT_TOOL, self.control_panel_tool_click, id = self.icnControlPanel.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnImgPaint( self, event ):
		event.Skip()
	
	def control_panel_tool_click( self, event ):
		event.Skip()
	

###########################################################################
## Class ctrlFrame
###########################################################################

class ctrlFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"SFLD Tree Viewer - Controls", pos = wx.Point( -1,-1 ), size = wx.Size( 886,645 ), style = wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP|wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.m_notebook1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		self.m_panel2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFile = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Tree File", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lblFile.Wrap( -1 )
		self.lblFile.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.lblFile.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer4.Add( self.lblFile, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer4.AddSpacer( ( 43, 0), 0, wx.EXPAND, 5 )
		
		self.m_FilePicker_tree = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, u"C:\\Users\\Michael\\Grad School Stuff\\Research\\Phylogenetics\\results\\2016-01-protein-sfld\\sf1\\sf1.tre", u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		self.m_FilePicker_tree.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer4.Add( self.m_FilePicker_tree, 1, wx.ALL, 5 )
		
		self.btn_import_tree = wx.Button( self.m_panel2, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.btn_import_tree, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.lblFile1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Taxon Metadata", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.lblFile1.Wrap( -1 )
		self.lblFile1.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		self.lblFile1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer5.Add( self.lblFile1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_FilePicker_annotation = wx.FilePickerCtrl( self.m_panel2, wx.ID_ANY, u"C:\\Users\\Michael\\Grad School Stuff\\Research\\Phylogenetics\\results\\2016-01-protein-sfld\\sf1\\sfld_superfamily_1_excel.tsv", u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		self.m_FilePicker_annotation.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizer5.Add( self.m_FilePicker_annotation, 1, wx.ALL, 5 )
		
		self.btn_import_annotation = wx.Button( self.m_panel2, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.btn_import_annotation, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
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
		
		self.m_staticline3 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Saving Images:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 11, 72, 90, 92, False, "Cambria" ) )
		self.m_staticText6.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer3.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Save Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		self.m_staticText9.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer13.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textImageSaveTarget = wx.TextCtrl( self.m_panel2, wx.ID_ANY, u"(file name)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textImageSaveTarget.SetToolTipString( u"file is saved in the working directory above automatically" )
		
		bSizer13.Add( self.m_textImageSaveTarget, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button1 = wx.Button( self.m_panel2, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.m_button1, 0, wx.ALL, 5 )
		
		
		bSizer7.Add( bSizer13, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer3 )
		self.m_panel2.Layout()
		bSizer3.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"Files", False )
		self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetBackgroundColour( wx.Colour( 200, 200, 200 ) )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Annotation Properties", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 11, 72, 90, 92, False, "Cambria" ) )
		
		bSizer11.Add( self.m_staticText7, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer121 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText71 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Field to Annotate", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )
		bSizer121.Add( self.m_staticText71, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_ComboSelectedFieldChoices = []
		self.m_ComboSelectedField = wx.ComboBox( self.m_panel4, wx.ID_ANY, u"(select)", wx.DefaultPosition, wx.DefaultSize, m_ComboSelectedFieldChoices, 0 )
		bSizer121.Add( self.m_ComboSelectedField, 1, wx.ALL, 5 )
		
		
		bSizer11.Add( bSizer121, 0, wx.EXPAND, 5 )
		
		self.m_staticline5 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer11.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer1211 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText711 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Circle Size (px)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText711.Wrap( -1 )
		bSizer1211.Add( self.m_staticText711, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_slider1 = wx.Slider( self.m_panel4, wx.ID_ANY, 2, 1, 10, wx.Point( -1,-1 ), wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_LABELS|wx.SIMPLE_BORDER )
		bSizer1211.Add( self.m_slider1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer11.Add( bSizer1211, 0, wx.EXPAND, 5 )
		
		self.m_button4 = wx.Button( self.m_panel4, wx.ID_ANY, u"Trigger Redraw", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.m_button4, 0, wx.ALL, 5 )
		
		
		bSizer11.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer10.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Values", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( 11, 72, 90, 92, False, "Cambria" ) )
		
		bSizer12.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		self.m_panel5 = wx.Panel( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL|wx.VSCROLL )
		self.m_panel5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_panel5.SetBackgroundColour( wx.Colour( 255, 244, 234 ) )
		self.m_panel5.SetMaxSize( wx.Size( 300,-1 ) )
		
		bSizer12.Add( self.m_panel5, 1, wx.ALL|wx.EXPAND, 1 )
		
		
		bSizer10.Add( bSizer12, 3, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer10 )
		self.m_panel4.Layout()
		bSizer10.Fit( self.m_panel4 )
		self.m_notebook1.AddPage( self.m_panel4, u"Node Annotation", False )
		self.m_Viewer = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook1.AddPage( self.m_Viewer, u"Edge Annotation", False )
		self.m_panel8 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText10 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Commands", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		bSizer15.Add( self.m_staticText10, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_textCtrl3 = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl3.SetMinSize( wx.Size( 500,50 ) )
		
		bSizer15.Add( self.m_textCtrl3, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel8.SetSizer( bSizer15 )
		self.m_panel8.Layout()
		bSizer15.Fit( self.m_panel8 )
		self.m_notebook1.AddPage( self.m_panel8, u"Console", False )
		self.m_panel51 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.FULL_REPAINT_ON_RESIZE|wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel6 = ViewAreaSelectorPanel( self.m_panel51, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
		self.m_panel6.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_panel6.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_panel6.SetMinSize( wx.Size( 400,300 ) )
		
		bSizer14.Add( self.m_panel6, 0, wx.ALL, 5 )
		
		
		self.m_panel51.SetSizer( bSizer14 )
		self.m_panel51.Layout()
		bSizer14.Fit( self.m_panel51 )
		self.m_notebook1.AddPage( self.m_panel51, u"Viewer", True )
		
		bSizer2.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_ACTIVATE, self.propogate_values )
		self.Bind( wx.EVT_CLOSE, self.on_frame_close )
		self.Bind( wx.EVT_ICONIZE, self.on_frame_iconize )
		self.m_FilePicker_tree.Bind( wx.EVT_FILEPICKER_CHANGED, self.set_file )
		self.btn_import_tree.Bind( wx.EVT_BUTTON, self.import_tree )
		self.m_FilePicker_annotation.Bind( wx.EVT_FILEPICKER_CHANGED, self.set_annotation_file )
		self.btn_import_annotation.Bind( wx.EVT_BUTTON, self.import_annotation )
		self.m_button1.Bind( wx.EVT_LEFT_UP, self.SaveCurrentImage )
		self.m_ComboSelectedField.Bind( wx.EVT_COMBOBOX, self.populate_annotation_values )
		self.m_ComboSelectedField.Bind( wx.EVT_TEXT, self.populate_annotation_values )
		self.m_slider1.Bind( wx.EVT_SCROLL, self.trigger_redraw )
		self.m_button4.Bind( wx.EVT_BUTTON, self.trigger_redraw )
		self.m_panel51.Bind( wx.EVT_PAINT, self.on_zoompanel_paint )
		self.m_panel6.Bind( wx.EVT_PAINT, self.on_img_paint )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def propogate_values( self, event ):
		event.Skip()
	
	def on_frame_close( self, event ):
		event.Skip()
	
	def on_frame_iconize( self, event ):
		event.Skip()
	
	def set_file( self, event ):
		event.Skip()
	
	def import_tree( self, event ):
		event.Skip()
	
	def set_annotation_file( self, event ):
		event.Skip()
	
	def import_annotation( self, event ):
		event.Skip()
	
	def SaveCurrentImage( self, event ):
		event.Skip()
	
	def populate_annotation_values( self, event ):
		event.Skip()
	
	
	def trigger_redraw( self, event ):
		event.Skip()
	
	
	def on_zoompanel_paint( self, event ):
		event.Skip()
	
	def on_img_paint( self, event ):
		event.Skip()
	

