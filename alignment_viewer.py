import os, threading, sys
import wx, cairo, math
from align_ctrl import *
from alignment import *

class AlignmentControlPanel(WxfbAlignmentControlPanel):
    image_path = None
    ref_aln_path = None
    tree_path = None
    colors = {'A':None, 'C':None, 'G': None, 'T':None, 'U':None}
    annotation_dict = None

    #image borders:
    b_top=None
    b_bottom = None
    b_left = None
    b_right=None

    # image_parameters
    phylo_line_width = 1
    aln_start_col = 1
    aln_num_cols = 100

    def __init__(self,parent):
        WxfbAlignmentControlPanel.__init__(self,parent)
        self.image_frame = AlignmentImageFrame(self)
        self.image_frame.Show()
        self.cairo_drawer = CairoAlignmentDrawer()
        self.aln = None

    def import_alignment_and_tree( self, event = None):
        ap = self.m_AlnFile.GetPath()
        tp = self.m_TreeFile.GetPath()
        print ap
        print tp
        self.aln = MultipleSequenceAlignment(refpath=ap,treepath=tp,generic_coords=True)
        self.m_textAlnLength.SetValue(str(len(self.aln.msa_cols)))
        self.m_textAlnNumTaxa.SetValue(str(self.aln.numtaxa ))

        if self.m_AnnotationFile.GetPath() is not None and self.m_AnnotationFile.GetPath()<>'':
            self.parse_annotation_file()
        else:
            self.annotation_dict={}
            for i in self.aln.ref.keys():
                self.annotation_dict[i]=i

    def set_output_path( self, event =None):
        fn = self.m_textCairoImageFile.GetValue()
        if fn[-4:]<>".png":
            fn = fn + '.png'
        self.image_path = os.path.join(self.m_textCairoImgFolder.GetPath(),fn)

    def set_colors(self):
        cA = self.m_colourA.GetColour().Get()
        cC = self.m_colourC.GetColour().Get()
        cG = self.m_colourG.GetColour().Get()
        cT = self.m_colourT.GetColour().Get()
        aA = float(self.m_alphaA.GetValue())
        aC = float(self.m_alphaC.GetValue())
        aG = float(self.m_alphaG.GetValue())
        aT = float(self.m_alphaT.GetValue())
        self.colors['A']=(float(cA[0])/255.0, float(cA[1])/255.0, float(cA[2])/255.0, aA)
        self.colors['C'] = (float(cC[0]) / 255.0, float(cC[1]) / 255.0, float(cC[2]) / 255.0, aC)
        self.colors['G'] = (float(cG[0]) / 255.0, float(cG[1]) / 255.0, float(cG[2]) / 255.0, aG)
        self.colors['T'] = (float(cT[0]) / 255.0, float(cT[1]) / 255.0, float(cT[2]) / 255.0, aT)
        self.colors['U'] = (float(cT[0]) / 255.0, float(cT[1]) / 255.0, float(cT[2]) / 255.0, aT)
        self.colors['N'] = (.8, .8, .8, .8)
        self.colors['M'] = (.4, .4, .4, .4)

    def set_cairo_settings(self):
        self.set_colors()
        try:
            w = int(self.m_textCairoImgWidth.GetValue())
            self.cairo_drawer.W = w
        except:
            print "%s won't convert to an integer..." % self.m_textCairoImgWidth.GetValue()

        try:
            h = int(self.m_textCairoImgHeight.GetValue())
            self.cairo_drawer.H = h
        except:
            print "%s won't convert to an integer..." % self.m_textCairoImgHeight.GetValue()

        self.pct_to_alignment = float(self.m_textPctWidthToAlignment.GetValue()) / 100.0
        self.pct_to_phylogeny = float(self.m_textPctWidthToPhylogeny.GetValue()) / 100.0
        self.pct_to_names = 1-self.pct_to_alignment - self.pct_to_phylogeny
        self.n = self.aln.numtaxa

        self.b_bottom=float(self.m_borderBottom.GetValue())
        self.b_top = float(self.m_borderTop.GetValue())
        self.b_left = float(self.m_borderLeft.GetValue())
        self.b_right = float(self.m_borderRight.GetValue())

        self.phylo_line_width = float(self.m_textPhylogenyLineWidth.GetValue())
        self.aln_start_col = int(self.m_textStartColumn.GetValue())
        self.aln_num_cols = int(self.m_textNumColumns.GetValue())


        # Stuff in External Ojbects:
        self.set_output_path()
        self.image_frame.path = self.image_path
        self.cairo_drawer.path = self.image_path
        print '''
        Active Cairo Settings:
           -Size: %(W)s, %(H)s
           -Path: %(path)s
        ''' % self.cairo_drawer.get_settings()

    def on_batch_click( self, event=None ):
        tot_cols = len(self.aln.msa_cols)
        numcols = int(self.m_textNumColumns.GetValue())
        num_images = int(math.ceil(float(tot_cols)/float(numcols)))
        fn_pref = self.m_textCairoImageFile.GetValue()
        for i in range(num_images):
            st_col = str(1+numcols*i)
            self.m_textStartColumn.SetValue(st_col)
            self.m_textCairoImageFile.SetValue(fn_pref + '_start_' + st_col + '_n_' + str(numcols))
            self.draw_cairo()



    def call_draw_cairo_thread(self):
        t=threading.Thread(target=self.draw_cairo)
        t.start()

    def show_viewer(self):
        self.image_frame.Show()

    def draw_cairo( self, event=None):
        wx.CallAfter(self.show_viewer)
        print 'getting settings ready...'
        self.set_cairo_settings()
        self.cairo_drawer.init_graphic()
        b_v = self.b_top + self.b_bottom
        b_h = self.b_right + self.b_left
        segs = []
        actual_num_cols=min(self.aln_num_cols,len(self.aln.msa_cols)-self.aln_start_col)

        # Draw the Phylogeny
        for i in self.aln.segment_endpoints:
            segs.append((self.b_left+(1.0-i[0])*(self.cairo_drawer.W-b_v)*self.pct_to_phylogeny,
                        self.b_top+i[1]*(self.cairo_drawer.H-b_h),
                         self.b_left + (1.0-i[2]) * (self.cairo_drawer.W - b_v)*self.pct_to_phylogeny,
                         self.b_top + i[3] * (self.cairo_drawer.H - b_h)))

        # Draw the Alignment Characters (TODO-make it so we can scroll rather than just having to make a bigger and bigger png?
        left_limit = self.b_left+self.pct_to_phylogeny*(self.cairo_drawer.W-b_h)+float(self.m_textAlignmentPhylogenySpacerWidth.GetValue())
        right_limit = left_limit - float(self.m_textAlignmentPhylogenySpacerWidth.GetValue()) + (self.cairo_drawer.W-b_h)*self.pct_to_alignment
        print "leftlimit %s, rightlimit %s" % (left_limit,right_limit)
        top_limit = self.b_top
        bot_limit = self.cairo_drawer.H - self.b_bottom
        h_spacing = (right_limit-left_limit)/self.aln_num_cols
        v_spacing = (bot_limit - top_limit)/self.n

        rect_groups={'A':[], 'C':[], 'G':[], 'T':[], 'U':[], 'M':[], 'N':[]}

        for i in range(actual_num_cols):
            col = self.aln.msa_cols[self.aln_start_col+i-1]
            # for j in col.chars.keys():
            #     chval = col.chars[j][2]
            for j in col.chars.keys():
                # try:
                chval = col.chars[j][2]
                if chval not in rect_groups.keys():
                    rect_groups[chval]=[]
                    self.colors[chval] = (1.0,1.0,1.0,1.0)
                rect_groups[chval].append((left_limit+i*h_spacing,top_limit+j*v_spacing,h_spacing,v_spacing))
                # except:
                #     print 'error in colmn %s:' % j

        for i in rect_groups.keys():
            clr = self.colors[i]
            self.cairo_drawer.draw_boxes_one_color(rect_groups[i],clr)

        # Draw the Text Names:
        if self.annotation_dict is None:
            for i in range(self.n):
                lab=self.aln.node_order[i]
                self.cairo_drawer.draw_text((right_limit+2,top_limit+(i+1)*v_spacing),lab)
        else:
            for i in range(self.n):
                lab=self.aln.node_order[i]
                self.cairo_drawer.draw_text((right_limit+2,top_limit+(i+1)*v_spacing),self.annotation_dict[lab])


        print 'Drawing the image file'
        self.cairo_drawer.draw_line_set(segs,self.phylo_line_width)

        self.cairo_drawer.finish_graphic()
        self.image_frame.refresh_image()
        print 'Done making graphic'

    def parse_annotation_file(self):
        self.annotation_dict={}
        if self.m_AnnotationFile.GetPath() <> None and os.path.exists(self.m_AnnotationFile.GetPath()):
            f=open(self.m_AnnotationFile.GetPath())
            for line in f:
                if len(line)>0:
                    a= line.strip().split('\t')
                    self.annotation_dict[a[0]]='--'.join(a[1:5])
            f.close()
        else:
            self.annotation_dict=None


class AlignmentImageFrame(WxfbAlignmentImageFrame):
    path=None
    def __init__(self,parent):
        WxfbAlignmentImageFrame.__init__(self,parent)
        self.Maximize()

    def load(self,path):
        self.path=path
        self.refresh_image()

    def refresh_image( self, event=None ):
        if self.path <> None and os.path.exists(self.path):
            self.m_htmlWin1.LoadFile(self.path)
        else:
            print 'The file %s does not exist...' % self.path


class CairoAlignmentDrawer():
    W=None
    H=None
    path='resources/test_alignment.png'
    colors={
        'A':None,
        'C':None,
        'G':None,
        'T':None,
        'U':None,
        'M':None,
        'N':None
    }
    surf=None
    ctx=None

    def __init__(self,path=None):
        if path is not None:
            self.path=path
        pass

    def get_settings(self):
        args={}
        args['W'] = self.W
        args['H'] = self.H
        args['path'] = self.path

        return args

    def init_graphic(self):
        if self.surf is not None:
            del self.surf
        if self.ctx is not None:
            del self.ctx
        self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.W, self.H)
        self.ctx = cairo.Context(self.surf)
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(0, 0, self.W, self.H)
        self.ctx.fill()

    def draw_box(self,top_left,size,color):
        self.ctx.set_source_rgba(*color)
        self.ctx.rectangle(top_left[0],top_left[1],size[0],size[1])
        self.ctx.fill()

    def draw_text(self,bottom_left,text):
        # print 'drawing text \'%s\' at the point %s' %(text,str(bottom_left))
        self.ctx.set_source_rgba(0,0,0,1)
        self.ctx.move_to(*bottom_left)
        self.ctx.show_text(text)

    def draw_boxes_one_color(self,boxes,color):
        '''
        Draws many boxes that will be all of the same color.
        :param boxes: list of 4-tuples with (x,y,w,h) coordinates
        :param color: RGBA 4-tuple
        :return:
        '''
        self.ctx.new_path()
        self.ctx.set_source_rgba(*color)
        for i in boxes:
            self.ctx.rectangle(*i)
        self.ctx.fill()

    def draw_line_set(self,line_set,line_width=None):
        '''
        Draws a set of lines by way of sub-paths for every (x0, y0, x1, y1) point in the list
        :param line_set: [(x0,y0,x1,y1)_1,(x0,y0,x1,y1)_2, ...]

        '''
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.new_path()
        if line_width<>None:
            old_lw = self.ctx.get_line_width()
            self.ctx.set_line_width(line_width)

        for i in line_set:
            self.ctx.new_sub_path()
            self.ctx.move_to(i[0],i[1])
            self.ctx.line_to(i[2],i[3])
        self.ctx.stroke()
        self.ctx.set_line_width(old_lw)

    def finish_graphic(self):
        self.surf.write_to_png(self.path)

class AlignmentApp(wx.App):
    def OnInit(self):
        self.mainframe = AlignmentControlPanel(None)
        self.SetTopWindow(self.mainframe)
        self.mainframe.SetIcon(wx.Icon('resources/icnPhyloMain32.png'))
        self.mainframe.Show()
        return True

if __name__=='__main__':
    app = AlignmentApp()
    app.MainLoop()