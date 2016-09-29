# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.html

###########################################################################
## Class WxfbAlignmentControlPanel
###########################################################################

class WxfbAlignmentControlPanel ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Alignment Control Panel", pos = wx.DefaultPosition, size = wx.Size( 814,678 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer57 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook2 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel1 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Alignment Properties", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetFont( wx.Font( 11, 74, 90, 92, True, "Arial" ) )
		
		bSizer4.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		bSizer51 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText21 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"File", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		self.m_staticText21.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer51.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_AlnFile = wx.FilePickerCtrl( self.m_panel1, wx.ID_ANY, u"C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\mushrooms\\pasta_bw.wu_etal_smith_etal_raw.aln", u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer51.Add( self.m_AlnFile, 1, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer51, 0, wx.EXPAND, 5 )
		
		bSizer52 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText22 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Tree File", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		self.m_staticText22.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer52.Add( self.m_staticText22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_TreeFile = wx.FilePickerCtrl( self.m_panel1, wx.ID_ANY, u"C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\mushrooms\\raxml.wu_etal_smith_etal.tre", u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer52.Add( self.m_TreeFile, 1, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer52, 0, wx.EXPAND, 5 )
		
		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText40 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Data Type:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		bSizer31.Add( self.m_staticText40, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		m_comboBox1Choices = [ u"DNA", u"RNA" ]
		self.m_comboBox1 = wx.ComboBox( self.m_panel1, wx.ID_ANY, u"RNA", wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0 )
		self.m_comboBox1.SetSelection( 1 )
		bSizer31.Add( self.m_comboBox1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"Import Alignment and Tree", wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer31.Add( self.m_button1, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer31, 0, wx.EXPAND, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"# Taxa:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer5.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textAlnNumTaxa = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"(numtaxa)", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER )
		self.m_textAlnNumTaxa.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		self.m_textAlnNumTaxa.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer5.Add( self.m_textAlnNumTaxa, 1, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 0, wx.EXPAND, 5 )
		
		bSizer53 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText23 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Length", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		self.m_staticText23.SetMinSize( wx.Size( 100,-1 ) )
		
		bSizer53.Add( self.m_staticText23, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textAlnLength = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"(numtaxa)", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.NO_BORDER )
		self.m_textAlnLength.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		self.m_textAlnLength.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer53.Add( self.m_textAlnLength, 1, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer53, 0, wx.EXPAND, 5 )
		
		self.m_staticline4 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer311 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText41 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Annotation File", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		bSizer311.Add( self.m_staticText41, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_AnnotationFile = wx.FilePickerCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer311.Add( self.m_AnnotationFile, 1, wx.ALL|wx.EXPAND, 1 )
		
		
		bSizer4.Add( bSizer311, 0, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		bSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer30 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer3.Add( bSizer30, 1, wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer3 )
		self.m_panel1.Layout()
		bSizer3.Fit( self.m_panel1 )
		self.m_notebook2.AddPage( self.m_panel1, u"Dashboard", True )
		self. q = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self. q, wx.ID_ANY, u"Cairo Settings", wx.DefaultPosition, wx.Size( -1,22 ), 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 11, 74, 90, 92, True, "Arial" ) )
		
		bSizer14.Add( self.m_staticText7, 0, wx.ALL, 1 )
		
		self.m_staticText9 = wx.StaticText( self. q, wx.ID_ANY, u"Image Size:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer14.Add( self.m_staticText9, 0, wx.ALL, 1 )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer16.AddSpacer( ( 10, 0), 0, 0, 5 )
		
		self.m_staticText8 = wx.StaticText( self. q, wx.ID_ANY, u"Width", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer16.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_textCairoImgWidth = wx.TextCtrl( self. q, wx.ID_ANY, u"1800", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer16.Add( self.m_textCairoImgWidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_staticText10 = wx.StaticText( self. q, wx.ID_ANY, u"Height", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		bSizer16.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCairoImgHeight = wx.TextCtrl( self. q, wx.ID_ANY, u"1500", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer16.Add( self.m_textCairoImgHeight, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer14.Add( bSizer16, 0, wx.EXPAND, 1 )
		
		
		bSizer14.AddSpacer( ( 0, 10), 0, 0, 5 )
		
		self.m_staticText20 = wx.StaticText( self. q, wx.ID_ANY, u"Image Output:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		bSizer14.Add( self.m_staticText20, 0, wx.ALL, 1 )
		
		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText19 = wx.StaticText( self. q, wx.ID_ANY, u"Folder:", wx.DefaultPosition, wx.Size( 73,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText19.Wrap( -1 )
		bSizer28.Add( self.m_staticText19, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2 )
		
		self.m_textCairoImgFolder = wx.DirPickerCtrl( self. q, wx.ID_ANY, u"C:\\Users\\miken\\Projects\\vtk\\data", u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer28.Add( self.m_textCairoImgFolder, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer14.Add( bSizer28, 0, wx.EXPAND, 5 )
		
		bSizer29 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText211 = wx.StaticText( self. q, wx.ID_ANY, u"File Name:", wx.DefaultPosition, wx.Size( 75,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText211.Wrap( -1 )
		bSizer29.Add( self.m_staticText211, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_textCairoImageFile = wx.TextCtrl( self. q, wx.ID_ANY, u"test.png", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer29.Add( self.m_textCairoImageFile, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer14.Add( bSizer29, 0, wx.EXPAND, 5 )
		
		
		bSizer14.AddSpacer( ( 0, 10), 0, 0, 5 )
		
		self.m_staticText31 = wx.StaticText( self. q, wx.ID_ANY, u"Phylogeny Parameters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		bSizer14.Add( self.m_staticText31, 0, wx.ALL, 1 )
		
		bSizer281 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer281.AddSpacer( ( 15, 0), 0, 0, 5 )
		
		self.m_staticText32 = wx.StaticText( self. q, wx.ID_ANY, u"Line Width", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		bSizer281.Add( self.m_staticText32, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_textPhylogenyLineWidth = wx.TextCtrl( self. q, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer281.Add( self.m_textPhylogenyLineWidth, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer281.AddSpacer( ( 25, 0), 0, 0, 5 )
		
		self.m_staticText33 = wx.StaticText( self. q, wx.ID_ANY, u"Line Color:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText33.Wrap( -1 )
		bSizer281.Add( self.m_staticText33, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_colourPhylogeny = wx.ColourPickerCtrl( self. q, wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer281.Add( self.m_colourPhylogeny, 0, wx.ALL, 1 )
		
		
		bSizer14.Add( bSizer281, 0, wx.EXPAND, 5 )
		
		self.m_staticline3 = wx.StaticLine( self. q, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer14.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText222 = wx.StaticText( self. q, wx.ID_ANY, u"Alignment Parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText222.Wrap( -1 )
		bSizer14.Add( self.m_staticText222, 0, wx.ALL, 5 )
		
		bSizer291 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer291.AddSpacer( ( 15, 0), 0, 0, 5 )
		
		self.m_staticText2111 = wx.StaticText( self. q, wx.ID_ANY, u"Starting Column", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText2111.Wrap( -1 )
		bSizer291.Add( self.m_staticText2111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_textStartColumn = wx.TextCtrl( self. q, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer291.Add( self.m_textStartColumn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer291.AddSpacer( ( 10, 0), 0, 0, 5 )
		
		self.m_staticText21111 = wx.StaticText( self. q, wx.ID_ANY, u"# Columns", wx.DefaultPosition, wx.Size( -1,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText21111.Wrap( -1 )
		bSizer291.Add( self.m_staticText21111, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_textNumColumns = wx.TextCtrl( self. q, wx.ID_ANY, u"200", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer291.Add( self.m_textNumColumns, 0, wx.ALL, 1 )
		
		
		bSizer14.Add( bSizer291, 0, wx.EXPAND, 5 )
		
		bSizer292 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer292.AddSpacer( ( 15, 0), 0, 0, 1 )
		
		self.m_staticText34 = wx.StaticText( self. q, wx.ID_ANY, u"Margin to Aignment:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )
		bSizer292.Add( self.m_staticText34, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_textAlignmentPhylogenySpacerWidth = wx.TextCtrl( self. q, wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 25,-1 ), 0 )
		bSizer292.Add( self.m_textAlignmentPhylogenySpacerWidth, 0, wx.ALL, 1 )
		
		
		bSizer14.Add( bSizer292, 0, wx.EXPAND, 1 )
		
		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText28 = wx.StaticText( self. q, wx.ID_ANY, u"% width for Taxonomy", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )
		bSizer24.Add( self.m_staticText28, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textPctWidthToPhylogeny = wx.TextCtrl( self. q, wx.ID_ANY, u"20", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer24.Add( self.m_textPctWidthToPhylogeny, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer14.Add( bSizer24, 0, 0, 5 )
		
		bSizer241 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText281 = wx.StaticText( self. q, wx.ID_ANY, u"% width for Alignment", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText281.Wrap( -1 )
		bSizer241.Add( self.m_staticText281, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textPctWidthToAlignment = wx.TextCtrl( self. q, wx.ID_ANY, u"60", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer241.Add( self.m_textPctWidthToAlignment, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer14.Add( bSizer241, 0, 0, 5 )
		
		self.m_button2 = wx.Button( self. q, wx.ID_ANY, u"Redraw Cairo Image", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button2, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_BatchImageButton = wx.Button( self. q, wx.ID_ANY, u"Make Batch of Images", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_BatchImageButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer13.Add( bSizer14, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self. q, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer13.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer18.AddSpacer( ( 0, 22), 0, 0, 5 )
		
		self.m_staticText11 = wx.StaticText( self. q, wx.ID_ANY, u"Colors:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer18.Add( self.m_staticText11, 0, wx.ALL, 1 )
		
		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText13 = wx.StaticText( self. q, wx.ID_ANY, u"A:", wx.DefaultPosition, wx.Size( 25,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText13.Wrap( -1 )
		bSizer19.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.m_colourA = wx.ColourPickerCtrl( self. q, wx.ID_ANY, wx.Colour( 0, 127, 255 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer19.Add( self.m_colourA, 0, wx.ALL, 1 )
		
		self.m_staticText221 = wx.StaticText( self. q, wx.ID_ANY, u"alpha:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText221.Wrap( -1 )
		bSizer19.Add( self.m_staticText221, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_alphaA = wx.TextCtrl( self. q, wx.ID_ANY, u"1.0", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer19.Add( self.m_alphaA, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer18.Add( bSizer19, 0, 0, 5 )
		
		bSizer191 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText131 = wx.StaticText( self. q, wx.ID_ANY, u"C:", wx.DefaultPosition, wx.Size( 25,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText131.Wrap( -1 )
		bSizer191.Add( self.m_staticText131, 0, wx.ALL, 5 )
		
		self.m_colourC = wx.ColourPickerCtrl( self. q, wx.ID_ANY, wx.Colour( 233, 239, 0 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer191.Add( self.m_colourC, 0, wx.ALL, 1 )
		
		self.m_staticText2211 = wx.StaticText( self. q, wx.ID_ANY, u"alpha:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2211.Wrap( -1 )
		bSizer191.Add( self.m_staticText2211, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_alphaC = wx.TextCtrl( self. q, wx.ID_ANY, u"1.0", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer191.Add( self.m_alphaC, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer18.Add( bSizer191, 0, 0, 5 )
		
		bSizer1911 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1311 = wx.StaticText( self. q, wx.ID_ANY, u"G:", wx.DefaultPosition, wx.Size( 25,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText1311.Wrap( -1 )
		bSizer1911.Add( self.m_staticText1311, 0, wx.ALL, 5 )
		
		self.m_colourG = wx.ColourPickerCtrl( self. q, wx.ID_ANY, wx.Colour( 183, 255, 111 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer1911.Add( self.m_colourG, 0, wx.ALL, 1 )
		
		self.m_staticText2212 = wx.StaticText( self. q, wx.ID_ANY, u"alpha:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2212.Wrap( -1 )
		bSizer1911.Add( self.m_staticText2212, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_alphaG = wx.TextCtrl( self. q, wx.ID_ANY, u"1.0", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer1911.Add( self.m_alphaG, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer18.Add( bSizer1911, 0, 0, 5 )
		
		bSizer1912 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1312 = wx.StaticText( self. q, wx.ID_ANY, u"U/T:", wx.DefaultPosition, wx.Size( 25,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText1312.Wrap( -1 )
		bSizer1912.Add( self.m_staticText1312, 0, wx.ALL, 5 )
		
		self.m_colourT = wx.ColourPickerCtrl( self. q, wx.ID_ANY, wx.Colour( 255, 74, 74 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		bSizer1912.Add( self.m_colourT, 0, wx.ALL, 1 )
		
		self.m_staticText2213 = wx.StaticText( self. q, wx.ID_ANY, u"alpha:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2213.Wrap( -1 )
		bSizer1912.Add( self.m_staticText2213, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_alphaT = wx.TextCtrl( self. q, wx.ID_ANY, u"1.0", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer1912.Add( self.m_alphaT, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer18.Add( bSizer1912, 0, 0, 5 )
		
		
		bSizer18.AddSpacer( ( 0, 10), 0, 0, 5 )
		
		self.m_staticText35 = wx.StaticText( self. q, wx.ID_ANY, u"Image Borders:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText35.Wrap( -1 )
		bSizer18.Add( self.m_staticText35, 0, wx.ALL, 5 )
		
		bSizer301 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer301.AddSpacer( ( 15, 0), 0, 0, 5 )
		
		self.m_staticText36 = wx.StaticText( self. q, wx.ID_ANY, u"Top:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText36.Wrap( -1 )
		bSizer301.Add( self.m_staticText36, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_borderTop = wx.TextCtrl( self. q, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 30,-1 ), 0 )
		bSizer301.Add( self.m_borderTop, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_staticText37 = wx.StaticText( self. q, wx.ID_ANY, u"Bot.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText37.Wrap( -1 )
		bSizer301.Add( self.m_staticText37, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_borderBottom = wx.TextCtrl( self. q, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 25,-1 ), 0 )
		bSizer301.Add( self.m_borderBottom, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_staticText38 = wx.StaticText( self. q, wx.ID_ANY, u"Left", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText38.Wrap( -1 )
		bSizer301.Add( self.m_staticText38, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_borderLeft = wx.TextCtrl( self. q, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 25,-1 ), 0 )
		bSizer301.Add( self.m_borderLeft, 0, wx.ALL, 1 )
		
		self.m_staticText39 = wx.StaticText( self. q, wx.ID_ANY, u"Right", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )
		bSizer301.Add( self.m_staticText39, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		self.m_borderRight = wx.TextCtrl( self. q, wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 25,-1 ), 0 )
		bSizer301.Add( self.m_borderRight, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 1 )
		
		
		bSizer18.Add( bSizer301, 0, 0, 5 )
		
		
		bSizer13.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		
		self. q.SetSizer( bSizer13 )
		self. q.Layout()
		bSizer13.Fit( self. q )
		self.m_notebook2.AddPage( self. q, u"Controls", False )
		
		bSizer57.Add( self.m_notebook2, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer57 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button1.Bind( wx.EVT_BUTTON, self.import_alignment_and_tree )
		self.m_textCairoImgFolder.Bind( wx.EVT_DIRPICKER_CHANGED, self.set_output_path )
		self.m_textCairoImageFile.Bind( wx.EVT_TEXT, self.set_output_path )
		self.m_textStartColumn.Bind( wx.EVT_TEXT, self.set_output_path )
		self.m_button2.Bind( wx.EVT_BUTTON, self.draw_cairo )
		self.m_BatchImageButton.Bind( wx.EVT_BUTTON, self.on_batch_click )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def import_alignment_and_tree( self, event ):
		event.Skip()
	
	def set_output_path( self, event ):
		event.Skip()
	
	
	
	def draw_cairo( self, event ):
		event.Skip()
	
	def on_batch_click( self, event ):
		event.Skip()
	

###########################################################################
## Class WxfbAlignmentImageFrame
###########################################################################

class WxfbAlignmentImageFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Alignment Image", pos = wx.DefaultPosition, size = wx.Size( 950,766 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.m_toolBar1.Realize() 
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_htmlWin1 = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		bSizer2.Add( self.m_htmlWin1, 1, wx.ALL|wx.EXPAND, 1 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_ACTIVATE, self.refresh_image )
		self.Bind( wx.EVT_ACTIVATE_APP, self.refresh_image )
		self.Bind( wx.EVT_RIGHT_DOWN, self.refresh_image )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def refresh_image( self, event ):
		event.Skip()
	
	
	

