from controller import Controller
import colorsys, wx
__author__ = 'Michael'

def color_scale(value):
    V=1
    if value<.5:
        H=.6
        S=value/.5*.9
    else:
        S=.9
        H=.6+(value-.5)/.8-int(.2+(value-.5)/.8)
    rgb=colorsys.hsv_to_rgb(H,S,V)
    rgb_out=(int(255*rgb[0]),int(255*rgb[1]),int(255*rgb[2]))
    # print "value = " + str(value) + '\tHSV = ' + str((H,S,V)) + '\tRGB = ' + str(rgb)
    return rgb_out

def script_function(bw_ref):
    from my_globals import amato_qiime_root
    import os, json
    myf=open(os.path.join(amato_qiime_root,'place_repset_placement.json'),'r')
    stra=myf.read()
    myf.close()
    place = json.loads(stra)

    myotus=['New.ReferenceOTU264','New.ReferenceOTU28','New.ReferenceOTU296','New.ReferenceOTU22','4326866',
            'New.ReferenceOTU58','New.ReferenceOTU87','180999','300394','296278','New.CleanUp.ReferenceOTU124',
            '211066','269913','4366524','New.ReferenceOTU2628','New.ReferenceOTU51','308498','110836','147182',
            'New.CleanUp.ReferenceOTU401','291011','New.ReferenceOTU66','340642','111771','New.CleanUp.ReferenceOTU4697',
            'New.CleanUp.ReferenceOTU241','New.ReferenceOTU134','4314124','721569','105813','New.CleanUp.ReferenceOTU1989',
            '195029','New.ReferenceOTU160','4419504','269532','301375','640999','918313','New.ReferenceOTU154']

    placements={}
    for i in place['placements']:
        for j in i['nm']:
            if j[0] in myotus:
                placements[j[0]]=i['p'][0]

    print "placements:\t%s" % len(placements)
    if len(placements)>0:
        print placements[placements.keys()[0]]
    print "myotus:\t%s" % len(myotus)

    # tmp=bw_ref.radial_phylogram.myt.find_node_with_label(str(placements[placements.keys()[0]][0]))
    # print tmp.__dict__
    # print tmp.viewer_node.__dict__
    # print tmp.edge.__dict__
    # print tmp.edge.viewer_edge.__dict__
    for i in placements.keys():
        nd = bw_ref.radial_phylogram.myt.find_node_with_label(str(placements[i][0]))
        frac=placements[i][3]/nd.edge.length
        hx = nd.edge.viewer_edge.head_x
        tx = nd.edge.viewer_edge.tail_x
        circ_x = (frac*hx[0]+(1-frac)*tx[0],frac*hx[1]+(1-frac)*tx[1])
        bw_ref.AddToExtraDrawCircles((circ_x,255,0,0,2))
    print '%s circles drawn' % len(bw_ref.ExtraDrawCircles)


    # titer=bw_ref.radial_phylogram.myt.postorder_node_iter()
    # for i in range(10):
    #     a=titer.next()
    #     print a.__dict__


def script_function_proteinstruct( prefix, scores=None, header = None):
    if scores==None:
        sc, hD=get_scores_by_method()
        scores=sc[prefix]
    import wx
    ctrl = Controller()
    fo = 'C:\\Users\\Michael\\Grad School Stuff\\Research\\Phylogenetics\\results\\2016-02-protein-alignment'
    fi = fo + '/scop/' + prefix + '_upp_alignment_masked.fasttree'
    ann_fi = fo + '/annotations/' + prefix + '_taxa.txt'
    ctrl.image_frame.control_panel.m_FilePicker_tree.SetPath(fi)
    ctrl.image_frame.control_panel.set_file()

    ctrl.image_frame.control_panel.m_FilePicker_annotation.SetPath(ann_fi)
    ctrl.image_frame.control_panel.set_annotation_file()
    # raw_input()
    ctrl.image_frame.control_panel.import_tree()
    ctrl.image_frame.control_panel.import_annotation()
    # raw_input()
    ctrl.image_frame.control_panel.m_ComboSelectedField.SetValue("source")
    ctrl.trigger_refresh()
    # raw_input()

    value_a=None
    for i in ctrl.image_frame.control_panel.value_picker.value_pickers:
        cols=[wx.Colour(15,240,234),wx.Colour(255,200,145)]
        cols_vivid=[wx.Colour(0,0,255),wx.Colour(255,0,0)]
        if value_a is None and i.value[0]=='Q':
            # print str(value_a) +'\t1'
            value_a=i.value[2:8]
            i.m_colourPicker1.SetColour(cols_vivid[0])
            i.m_spinCtrl.SetValue(3)
            i.clr=cols_vivid[0]
            i.size=3
        elif value_a is None and i.value[0]!='Q':
            # print str(value_a) +'\t2'
            value_a=i.value[0:6]
            i.m_colourPicker1.SetColour(cols[0])
            i.m_spinCtrl.SetValue(8)
            i.clr=cols[0]
            i.size=8
        elif value_a is not None and i.value[0]=='Q' and i.value[2:8]==value_a:
            # print str(value_a) +'\t' + i.value[2:8] + '\t3'
            i.m_colourPicker1.SetColour(cols_vivid[0])
            i.m_spinCtrl.SetValue(3)
            i.clr=cols_vivid[0]
            i.size=3
        elif value_a is not None and i.value[0]!='Q' and i.value[0:6]==value_a:
            # print str(value_a) +'\t' + i.value[0:6] + '\t4'
            i.m_colourPicker1.SetColour(cols[0])
            i.m_spinCtrl.SetValue(8)
            i.clr=cols[0]
            i.size=8
        elif value_a is not None and i.value[0]=='Q' and i.value[2:8]!=value_a:
            # print str(value_a) +'\t' + i.value[2:8] + '\t5'
            i.m_colourPicker1.SetColour(cols_vivid[1])
            i.m_spinCtrl.SetValue(3)
            i.clr=cols_vivid[1]
            i.size=3
        elif value_a is not None and i.value[0]!='Q' and i.value[0:6]!=value_a:
            # print str(value_a) +'\t' + i.value[0:6] + '\t6'
            i.m_colourPicker1.SetColour(cols[1])
            i.m_spinCtrl.SetValue(8)
            i.clr=cols[1]
            i.size=8
        i.m_checkBox1.SetValue(True)
        i.process_annotationvalue_check()


    ctrl.trigger_refresh()
    ctrl.image_frame.draw_text(prefix)

    #draw rectangles
    w=50
    h=50
    x=1100
    y=50
    rects=[]
    methods=['HHa', 'HE', 'H+U', 'HE+U', 'UPP']
    for i in range(5):
        a=scores[i]
        if a=='':
            a=0
            ctrl.image_frame.draw_text("n/a",x,y+h+2,wx.Font(11,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        else:
            ctrl.image_frame.draw_text("%0.3f" % float(a),x,y+h+2,wx.Font(11,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        mycolor=color_scale(float(a))
        alpha=.5
        rects.append((x,y,w,h,mycolor,alpha))
        ctrl.image_frame.draw_text(methods[i],x,30,wx.Font(11,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        # ctrl.image_frame.draw_text("%0.3f" % float(a),x,y+h+2,wx.Font(11,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

        x+=w
    ctrl.image_frame.draw_rectangles(rects)
    a=wx.Bitmap('C:\\Users\\Michael\\Dropbox\\Grad School\\Phylogenetics\\work\\protein-alignment\\results\\color_scale.png',wx.BITMAP_TYPE_PNG)
    ctrl.image_frame.memdc.SelectObject(ctrl.image_frame.current_bitmap)
    ctrl.image_frame.memdc.DrawBitmap(a,x+30,50)
    ctrl.image_frame.memdc.SelectObject(wx.NullBitmap)
    ctrl.image_frame.draw_text("scale:",x+30,30,wx.Font(11,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

    img_fi=fo + '/images/' + prefix + '.jpg'
    ctrl.image_frame.save_dc_to_bitmap(img_fi)


def script_function_container():
    fo = 'C:\\Users\\Michael\\Grad School Stuff\\Research\\Phylogenetics\\results\\2016-02-protein-alignment\\taxa'
    scores,header=get_scores_by_method()
    import os, time
    for i in os.listdir(fo):
        a=i.replace('_taxa.txt','')
        print a
        script_function(a)
        # time.sleep(2)

def get_scores_by_method():
    scoresfile='C:\\Users\\Michael\\Dropbox\\Grad School\\Phylogenetics\\work\\protein-alignment\\results\\results-by-method.csv'
    myf=open(scoresfile,'r')
    header=myf.readline()
    scores={}
    for i in myf:
        a=i.strip().split(',')
        scores[a[0]]=(a[1],a[2],a[3],a[4],a[5])     #hhalign_default,hhalign_ensemble_default,hhalign_upp,hhalign_ensemble_upp,upp
    return (scores,header)

def test_alphas():
    ctrl = Controller()
    mycolor1=color_scale(float(.5))
    mycolor2=color_scale(float(.8))
    # alpha=wx.ALPHA_TRANSPARENT
    alpha=0.5
    rects=[]
    x=400
    y=400
    h=100
    w=100
    rects.append((x,y,w,h,mycolor2,alpha))
    x+=int(w/2)
    rects.append((x,y,w,h,mycolor1,alpha))
    ctrl.image_frame.draw_rectangles(rects)

def make_hocr_race():
    ctrl=Controller()
