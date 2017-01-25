import math
import numpy as np
import random
import colorsys
import platform



def get_random_color(incr=None):
    if incr is None:
        H=random.random()
    else:
        H=incr+.03+random.random()*.08
    while True:
        S=random.random()*.5 + .5
        V=random.random()*.5 + .5
        if S+V>1.5:
            break
    rgb=colorsys.hsv_to_rgb(H,S,V)
    return rgb

def write_list_to_file(mylist,filepath):
    myf=open(filepath,'w')

    for i in mylist:
        myf.write(i + '\n')

    myf.close()

def color_scale_set(total, as_ints=True):
    lower_lim = .40

    side = int(float(total) ** .333 + 1)
    # print 'side length: %s' % side
    gap = 1.0 / float(side)

    #get the number of ineligible points (in the dark part of the cube
    ineliglbe_pts = int((lower_lim - gap * 5 / 6) / gap + 1) ** 3
    ineliglbe_pts += 1 #white is not allowed

    while side ** 3 - ineliglbe_pts < total:
        side += 1
        gap = 1.0 / float(side)
        ineliglbe_pts = int((lower_lim - gap * 5 / 6) / gap + 1) ** 3
    # print 'adjusted # pts: %s' % (side ** 3 - ineliglbe_pts )

    coords = []
    for i in range(side):
        c = gap * 5 / 6 + gap * float(i)
        coords.append(c)

    locus = []
    backrange = range(side)
    backrange.sort(reverse=True)
    for i in backrange:
        for j in backrange:
            for k in backrange:
                newc = (coords[i], coords[j], coords[k])
                if max(newc) > lower_lim and min(i,j,k)<max(backrange):
                    locus.append(newc)

    sss = side * side * side - ineliglbe_pts
    # print 'sss: %s' % sss
    # print 'length of locus (locus): %s' % len(locus)
    perm = get_ideal_permutation(len(locus))
    finals = []
    for i in perm:
        finals.append(locus[len(perm) - i - 1])
    if as_ints==True:
        finals2 = []
        for i in finals:
            finals2.append((int(i[0]*255), int(i[1]*255), int(i[2]*255)))
        return finals2
    else:
        return finals



def get_ideal_permutation(els):
    random.seed(100)
    m1 = int(els / 2)
    m2 = m1 + 1
    Ai = range(1, m1)
    Bi = range(m2 + 1, els + 1)
    A = random.sample(Ai, len(Ai))
    B = random.sample(Bi, len(Bi))
    out = []
    out.append(m1 - 1)
    if len(B) <> len(A):
        out.append(B.pop() - 1)
    for i in range(len(A)):
        out.append(A.pop() - 1)
        out.append(B.pop() - 1)
    out.append(m2 - 1)
    return out

# colors=[(240,163,255),(0,117,220),(153,63,0),(76,0,92),(25,25,25),(0,92,49),(43,206,72),(255,204,153),(128,128,128),(148,255,181),(143,124,0),(157,204,0),(194,0,136),(0,51,128),(255,164,5),(255,168,187),(66,102,0),(255,0,16),(94,241,242),(0,153,143),(224,255,102),(116,10,255),(153,0,0),(255,255,128),(255,255,0),(255,80,5)]

''' citation for this color set: http://godsnotwheregodsnot.blogspot.ru/2012/09/color-distribution-methodology.html
'''
colors = [(0,255,0),(0,0,255),(255,0,0),(1,255,254),(255,166,254),(255,219,102),(0,100,1),(1,0,103),(149,0,58),
          (0,125,181),(255,0,246),(255,238,232),(119,77,0),(144,251,146),(0,118,255),(213,255,0),(255,147,126),
          (106,130,108),(255,2,157),(254,137,0),(122,71,130),(126,45,210),(133,169,0),(255,0,86),(164,36,0),(0,174,126),
          (104,61,59),(189,198,255),(38,52,0),(189,211,147),(0,185,23),(158,0,142),(0,21,68),(194,140,159),
          (255,116,163),(1,208,255),(0,71,84),(229,111,254),(120,130,49),(14,76,161),(145,208,203),(190,153,112),
          (150,138,232),(187,136,0),(67,0,44),(222,255,116),(0,255,198),(255,229,2),(98,14,0),(0,143,156),(152,255,82),
          (117,68,177),(181,0,255),(0,255,120),(255,110,65),(0,95,57),(107,104,130),(95,173,78),(167,87,64),(165,255,210),
          (255,177,103),(0,155,255),(232,94,190),(0,0,0)]
phylum_orders={'Proteobacteria':1,'Actinobacteria':2,'Firmicutes':3,'Bacteroidetes':4,'Tenericutes':5,
'Spirochaetes':6,'Deinococcus-Thermus':7,'Streptophyta':8,'Verrucomicrobia':9,'Thermotogae':10,
'Fusobacteria':11,'Aquificae':12,'Acidobacteria':13,'Chloroflexi':14,'Synergistetes':15,'Planctomycetes':16,
'Chlamydiae':17,'Deferribacteres':18,'Chlorobi':19,'#N/A':20,'Chlorophyta':21,'Nitrospirae':22,'Thermodesulfobacteria':23,
'Cyanobacteria':24,'Chrysiogenetes':25,'Fibrobacteres':26,'Armatimonadetes':27,'Lentisphaerae':28,'Bacillariophyta':29,
'Dictyoglomi':30,'Euglenida':31,'Elusimicrobia':32,'Gemmatimonadetes':33,'Caldiserica':34,'Ignavibacteriae':35,
'proteobacteria':1,'actinobacteria':2,'firmicutes':3,'bacteroidetes':4,'tenericutes':5,'spirochaetes':6,
'deinococcus-thermus':7,'verrucomicrobia':9,'thermotogae':10,'fusobacteria':11,'aquificae':12,'acidobacteria':13,
'chloroflexi':14,'synergistetes':15,'planctomycetes':16,'chlamydiae':17,'deferribacteres':18,'chlorobi':19,
'nitrospira':22,'thermodesulfobacteria':23,'cyanobacteria_chloroplast':24,'chrysiogenetes':25,
'fibrobacteres':26,'armatimonadetes':27,'lentisphaerae':28,'dictyoglomi':30,'elusimicrobia':32,
'gemmatimonadetes':33,'caldiserica':34}


def np_do_two_segments_intersect(a,b):
    '''
    Returns true if segments a and b intersect. Also returns the parametric indices [t1,t2] of the intersection point, if it exists.
    Segments are defined like: a=[x1,y1,x2,y2]

    NOTE: the segments touching is not good enough. They need to intersect in the open set between the endpoints.
    :param a:
    :param b:
    :return:
    '''

    #not a line, we'll call that false and move on...
    if ((a[0]==a[2]) and (a[1]==a[3])) or ((a[0]==a[2]) and (a[1]==a[3])):
        return False, a,b
    if ((a[0]==b[0] and a[1]==b[1]) or (a[0]==b[2] and a[1]==b[3]) or (a[2]==b[0] and a[3]==b[1])or (a[2]==b[2] and a[3]==b[3])):
        return False, a,b
    m1=np.dot(np.vstack((a[2:4]-a[0:2],b[2:4]-b[0:2])).transpose(),np.array([[1,0],[0,-1]],dtype=np.float64))

    m2 = b[0:2]-a[0:2]
    try:
        # matrix is full rank, solve away...
        t = np.dot(np.linalg.inv(m1),m2)
        return np.all((t>0.)*(t<1.)), t[0], t[1]
    except np.linalg.linalg.LinAlgError:
        # ugh, edge cases
        if a[2]==a[0]:
            t2 = (b[1] - a[1]) / (a[3] - a[1])
            t4 = (b[3] - a[1]) / (a[3] - a[1])
            return (b[0]==a[0] and ((t2>0 and t2<1) or (t4>0 and t4 <1))), a, b
        if a[1]==a[3]:
            t1 = (b[0] - a[0]) / (a[2] - a[0])
            t3 = (b[2] - a[0]) / (a[2] - a[0])
            return (b[1]==a[1] and ((t1>0 and t1<1) or (t3>0 and t3 <1))), a, b
        t1=(b[0]-a[0])/(a[2]-a[0])
        t2 = (b[1]-a[1]) / (a[3] - a[1])
        t3 = (b[2] - a[0])/ (a[2] - a[0])
        t4 = (b[3]-a[1]) / (a[3] - a[1])
        return (t1>0 and t1==t2 and t1<1) or (t3>0 and t3==t4 and t3<1), (t1,t2,t3,t4)




def get_list_from_file(filepath):
    myf=open(filepath,'r')
    ol=[]
    for i in myf:
        if i.strip()<>'':
            ol.append(i.strip())

    myf.close()
    return ol

def distance_btw_points(pt1,pt2):
    # print pt1
    # print pt2
    # print "%s" % ((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)
    return math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)

def dot_product(v1, v2):
    return v1[0]*v2[0]+v1[1]*v2[1]

if platform.system()=='Windows':
    import c_utilities as cutils
    def np_find_intersect_segments(segs):
        return cutils.np_find_intersect_segments_c(segs)

    def np_find_intersect_segments_test(segs):
        return cutils.np_find_intersect_segments_c_test(segs)

else:
    def np_find_intersect_segments(segs):
        res = np_find_intersect_segments_allpy(segs)
        return res[0]

def np_find_intersect_segments_allpy(segs):
    '''
    implements the sweep-line algorithm to find out if any of a list of line segments intersect.
    :param segs:
    :return:
    '''

    numpts = segs.shape[0]
    '''These arrays are laid out as (x,y,left?,index) where left is 1 if the point is a left point
    '''

    left_pts = np.zeros((numpts,2),dtype=np.float64)
    left_inds = np.vstack((np.zeros(numpts,dtype=np.int8),np.arange(numpts, dtype=np.int32))).transpose()
    right_pts = np.zeros((numpts, 2), dtype=np.float64)
    right_inds = np.vstack((np.ones(numpts,dtype=np.int8),np.arange(numpts, dtype=np.int32))).transpose()

    left_pts[:, 0] = np.where(segs[:, 0] > segs[:, 2], segs[:, 2], segs[:, 0])
    left_pts[:, 1] = np.where(segs[:, 0] > segs[:, 2], segs[:, 3], segs[:, 1])
    right_pts[:, 0] = np.where(segs[:, 0] > segs[:, 2], segs[:, 0], segs[:, 2])
    right_pts[:, 1] = np.where(segs[:, 0] > segs[:, 2], segs[:, 1], segs[:, 3])
    # for i in range(numpts):
    #     if segs[i,0]>segs[i,2]:
    #         left_pts[i, 0:2] = segs[i, 2:4]
    #         right_pts[i, 0:2] = segs[i, 0:2]
    #     else:
    #         right_pts[i, 0:2] = segs[i, 2:4]
    #         left_pts[i, 0:2] = segs[i, 0:2]
    ordered_segs = np.hstack((left_pts,right_pts)).copy()
    # print ordered_segs


    all_pts = np.vstack((left_pts,right_pts))
    all_inds = np.vstack((left_inds,right_inds))

    all_view = np.array(np.zeros(2*numpts),dtype=[('x','f8'),('y','f8'),('left','i1'),('ind','i4')])
    all_view['x']=all_pts[:,0]
    all_view['y'] = all_pts[:, 1]
    all_view['left'] = all_inds[:,0]
    all_view['ind'] = all_inds[:,1]
    sort_inds = np.argsort(all_view,order=['x','left'])

    all_pts = all_pts[sort_inds]
    all_inds = all_inds[sort_inds]
    active_segs=None

    start_pt = 0
    wait=True
    while(wait):
        if all_inds[start_pt,1] != all_inds[start_pt+1,1]:
            wait=False
            if np_do_two_segments_intersect(ordered_segs[all_inds[start_pt,1],:],ordered_segs[all_inds[start_pt+1,1],:])==True:
                return False,ordered_segs[all_inds[start_pt,1],:],ordered_segs[all_inds[start_pt+1,1],:]
            active_segs = np.hstack((ordered_segs[all_inds[start_pt, 1], :], all_inds[start_pt, 1])).reshape((1, 5))
        else:
            start_pt +=2
            if start_pt >= all_inds.shape[0]:
                # print 'condition: start'
                return True, None, None

    for i in range(start_pt+1,2*numpts):
        nact = int(active_segs.shape[0])
        if all_inds[i,0]==0:
            k=sum(active_segs[:,1]<all_pts[i,1])

            pt = ordered_segs[all_inds[i,1],:]
            active_segs=np.insert(active_segs,k,np.hstack((ordered_segs[all_inds[i,1],:],all_inds[i,1])),0)
            if k>0:
                pred = active_segs[k-1,0:4]
                time_to_quit=np_do_two_segments_intersect(pt,pred)
                if time_to_quit[0]==True:

                    return False, pt ,pred
            if k<(nact-1):

                succ = active_segs[k+1,0:4]

                time_to_quit=np_do_two_segments_intersect(pt,succ)
                if time_to_quit[0]==True:
                    return False, pt, succ


        else:
            # try:
            # k=active_inds.pop(all_inds[i,1])
            try:
                k=np.asscalar(np.where(active_segs[:,4]==all_inds[i,1])[0])
            except:
                print 'error at that ascalar command'

                import sys
                sys.exit(0)
            if k < (nact-1) and k > 0:
                time_to_quit=np_do_two_segments_intersect(active_segs[k-1,0:4],active_segs[k+1,0:4])
                if time_to_quit[0]==True:
                    return False, active_segs[k-1,0:4],active_segs[k+1,0:4]
            active_segs=np.delete(active_segs,k,0)
    return True, None, None

def distance_to_line_segment(segx1, segx2, pt):
    diff = (segx2[0]-segx1[0],segx2[1]-segx1[1])
    v1 = (pt[0]-segx1[0],pt[1]-segx1[1])
    v2 = (pt[0] - segx2[0], pt[1] - segx2[1])
    #
    # print dot_product(diff,v1)
    # print dot_product(diff, v2)
    # print distance_btw_points(segx1,pt)
    # print distance_btw_points(segx2,pt)

    if dot_product(v1,diff)*dot_product(v2,diff) < 0:
        return abs((segx2[1]-segx1[1])*pt[0] - (segx2[0]-segx1[0])*pt[1] + segx2[0]*segx1[1]-segx2[1]*segx1[0])/distance_btw_points(segx1,segx2)
    else:
        return min(distance_btw_points(segx1,pt),distance_btw_points(segx2,pt))

def convert_coordinates(xyrange, disprange, xycoords):
    '''
    Converts coordinates from the x-y plan based on the range "xyrange" (xmin, xmax, ymin, ymax) to the display coordinates

    :param xyrange: (xmin, xmax, ymin, ymax)
    :param disprange: (w , h) (indexed at 0, so max output will be (w-1, h-1)
    :param xycoords: (x,y)
    :return: display coords (on numpy scale) or None if it's out of the display range
    '''
    aspect_ratio=float(disprange[0])/float(disprange[1])
    old_aspect_ratio=float(xyrange[1]-xyrange[0])/float(xyrange[3]-xyrange[2])

    if old_aspect_ratio>aspect_ratio:
        # old width becomes new width, old height is centered:
        scale=(disprange[0]-1)/(xyrange[1]-xyrange[0])
        gap=(float(disprange[1]-1)-float(xyrange[3]-xyrange[2])*scale)/2
        xnew = round(scale*(xycoords[0]-xyrange[0]), 0)
        ynew = disprange[1]-1 - round(gap+scale*float(xycoords[1]-xyrange[2]),0)
    else:
        # old height becomes new height, old width is centered
        scale=(disprange[1]-1)/(xyrange[3]-xyrange[2])
        gap=(float(disprange[0]-1)-float(xyrange[1]-xyrange[0])*scale)/2
        ynew = round(scale*(xycoords[1]-xyrange[2]),0)
        xnew = disprange[0]-1 - round(gap+scale*float(xycoords[0]-xyrange[0]),0)

    # xnew = round((disprange[0]-1)*(xycoords[0]-xyrange[0])/(xyrange[1]-xyrange[0]), 0)
    # ynew = disprange[1]-1 - round((disprange[1]-1)*(xycoords[1]-xyrange[2])/(xyrange[3]-xyrange[2]), 0)

    if xnew > disprange[0]-1 or xnew < 0 or ynew < 0 or ynew > disprange[1]-1:
        return (xnew,ynew,False)
    else:
        return (xnew,ynew,True)

def get_valid_points(pts,H,W):
    newpts=[]
    for i in pts:
        if (i[0]>=0) and (i[0]<=W-1) and (-i[1]>=0) and (-i[1]<=H-1):
            if i[0]>=min(pts[0][0],pts[1][0]) and i[0] <= max(pts[0][0],pts[1][0]) and -i[1]>=min(-pts[0][1],-pts[1][1]) and -i[1] <= max(-pts[0][1],-pts[1][1]):
                newpts.append(i)

    # assert len(newpts)==0 or len(newpts)==2, "AssertionError: number of valid points is %s" % len(newpts)
    if len(newpts)==0:
        return None
    elif len(newpts)==2:
        return tuple(newpts)
    else:
        print "Length of the points is not 0 or 2:"
        print "H\tW:"
        print "%s\t%s" % (H,W)
        for i in pts:
            print "%s\t%s" % i
        # print pts
        assert len(newpts)==0 or len(newpts)==2, "AssertionError: number of valid points is %s" % len(newpts)

def get_line_on_screen(x1,x2,H,W):
    '''
    Converts coordinates from the x-y plan based on the range "xyrange" (xmin, xmax, ymin, ymax) to the display coordinates

    :param xyrange: (xmin, xmax, ymin, ymax)
    :param disprange: (w , h) (indexed at 0, so max output will be (w-1, h-1)
    :param x1, x2: (x,y) coordinates of endpoints of the segment
    :return: display coords (on numpy scale) or None if it's out of the display range
    '''

    # print x1
    # print x2
    # print W
    # print H
    if (x1[0]<0 and x2[0]<0) or (x1[0] > (W-1) and x2[0] > W-1) or (-1*x1[1]<0 and -1*x2[1] < 0) or (-1*x1[1] > (H-1) and -1*x2[1] > (H-1)):
        return None
    elif x1[0]>=0 and x1[0]<=W-1 and -1*x1[1]>=0 and -1*x1[1]<=H-1 and x2[0]>=0 and x2[0]<=W-1 and -x2[1]>=0 and -x2[1]<=H-1:
        return (x1,x2)
    else:
        pts = []
        m=(x2[1]-x1[1])/(x2[0]-x1[0])
        pts.append(x1)
        pts.append(x2)
        if x1[0]==x2[0]:
            topside_wd = x2[0]
            pts.append((topside_wd, 0))
            bottomside_wd = x1[0]
            pts.append((bottomside_wd, -(H - 1)))


        if x1[1]==x2[1]:
            leftside_ht = x2[1]
            pts.append((topside_wd, 0))
            rightside_ht = x1[1]
            pts.append((bottomside_wd, -(H - 1)))
        if x1[0]<>x2[0]:
            m = (x2[1] - x1[1]) / (x2[0] - x1[0])
            leftside_ht=x1[1]-x1[0]*m
            pts.append((0,leftside_ht))
            rightside_ht=x2[1]+(W-x2[0])*m
            pts.append((W-1,rightside_ht))

        if x1[1]<>x2[1]:
            topside_wd=x2[0]-x2[1]/m
            pts.append((topside_wd,0))
            bottomside_wd = x1[0]-(x1[1]-H)/m
            pts.append((bottomside_wd,-(H-1)))

        newpts= get_valid_points(pts,H,W)
        return newpts

def convert_coordinates_new(max_dims,disprange,x1,x2):
    w=disprange[0]
    h=disprange[1]
    aspect=abs((max_dims[1]-max_dims[0])/(max_dims[3]-max_dims[2]))
    if aspect > (w/h):
        # constraining dimension is horizontal
        vgap = (h-w/aspect)/2
        hgap = 0
    else:
        #constraining dimension is horizontal
        vgap = 0
        hgap = (w-h*aspect)/2

    a=np.array(([max_dims[0],max_dims[2],1],[max_dims[0],max_dims[3],1],[max_dims[1],max_dims[3],1]),dtype=np.float64)
    ainv=np.linalg.inv(a)
    tx=np.dot(ainv,np.array([hgap,hgap,w-1-hgap],dtype=np.float64))
    t11=np.asscalar(tx[0])
    t12 = np.asscalar(tx[1])
    t13 = np.asscalar(tx[2])
    ty=np.dot(ainv,np.array([vgap-(h-1),-vgap,-vgap],dtype=np.float64))
    t21=np.asscalar(ty[0])
    t22=np.asscalar(ty[1])
    t23 = np.asscalar(ty[2])
    x1n = (t11 * x1[0] + t12 * x1[1] + t13, t21 * x1[0] + t22 * x1[1] + t23)
    x2n = (t11 * x2[0] + t12 * x2[1] + t13, t21 * x2[0] + t22 * x2[1] + t23)
    return get_line_on_screen(x1n,x2n,h,w)

def read_from_fasta(file_path):
    '''
    Reads a fasta file into a dictionary where the keys are sequence names and values are strings representing the
    sequence.

    :param file_path:
    :return:
    '''
    output={}
    fasta=open(file_path,'r')
    first=True
    for l in fasta:
        if l[0]=='>':
            if first<>True:
                output[name]=seq
            else:
                first=False
            name=l[1:].strip()
            seq=''
        else:
            seq=seq + l.strip()
    output[name]=seq
    fasta.close()
    return output

def rotate(x,theta):
    '''

    :param x: (x,y) ordered pair representing coordinates
    :param theta: rotation angle (in radians)
    :return:
    '''

    return (x[0]*math.cos(theta)-x[1]*math.sin(theta),x[0]*math.sin(theta)+x[1]*math.cos(theta))

def unit_test_line_on_screen():
    #case 0: all in the box
    xyrange = (0, 4, 0, 2)
    disprange = (500, 300)
    x1 = (1.5, 0.5)
    x2 = (3.3, 1)
    print "result should be:(187.13,211.75),(411.68,149.50)"
    print convert_coordinates_new(xyrange, disprange, x1, x2)
    print "\n"

    print "Case: One Outside Box"
    xyrange=(0,4,0,2)
    disprange=(500,300)
    x1=(1.5,2.5)
    x2=(3.3,1)
    print "result should be:(231.91,0.00),(411.68,149.50)"
    print convert_coordinates_new(xyrange,disprange,x1,x2)
    print "\n"

    print "Case: Two Outside Box"
    xyrange=(0,4,0,2)
    disprange=(500,300)
    x1=(1.5,2.5)
    x2=(4.5,1)
    print "result should be:(261.77,0.00),(500.00,118.87)"
    print convert_coordinates_new(xyrange,disprange,x1,x2)
    print "\n"


import wx
import controller
class ValuePickerControlGridBag(wx.GridBagSizer):
    def __init__(self,parent,*args):
        wx.GridBagSizer.__init__(self,wx.VERTICAL)
        # self.panel=wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL )
        # self.panel.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ))
        # self.panel.SetBackgroundColour( wx.Colour( 255, 234, 213 ))
        #
        # self.m_staticText8 = wx.StaticText( parent, wx.ID_ANY, u"Values", wx.DefaultPosition, wx.DefaultSize, 0 )
        # self.m_staticText8.Wrap( -1 )
        # self.m_staticText8.SetFont( wx.Font( 11, 72, 90, 92, False, "Cambria" ) )
        # self.Add(self.m_staticText8,0, wx.ALL,5)
        #
        # self.szr_ValuesVert = wx.BoxSizer( wx.VERTICAL )
        self.parent=parent
        self.value_pickers=[]
        self.values=None
        self.colors=None

        # self.set_values(['189'])

    def clear_all(self):
        self.Clear(True)
        self.values=[]
        self.value_pickers=[]

    def set_values(self,vals=None):
        self.clear_all()
        if vals != None:
            self.values=vals

        k=0

        self.colors={}
        for i in self.values:
            if k>=len(colors):
                clr=get_random_color()
            else:
                clr=colors[k]
                k+=1
            self.colors[i]=clr


            a=self.ValuePicker(self.parent,i,clr,val_ctrl=self)
            self.Add(a,0, wx.EXPAND, 5)
            self.value_pickers.append(a)

        self.add_final_spacer()

    def add_final_spacer(self):
        bSizer15 = wx.BoxSizer( wx.VERTICAL )
        bSizer15.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        self.Add( bSizer15, 1, wx.EXPAND, 5 )

    def move_to_bottom(self,val):
        val_temps=[]
        for i in self.value_pickers:
            args={'parent':self.parent, 'clr':i.clr, 'value':i.value, 'sz':i.size, 'checked':i.m_checkBox1.GetValue(), 'val_ctrl':self}
            val_temps.append(args)
        for v in val_temps:
            # print v
            if v['value']==val:
                ind=val_temps.index(v)
                tmp = val_temps.pop(ind)
                val_temps.append(tmp)
        self.load_values(val_temps)

    def load_values(self,val_temps):

        self.clear_all()
        mypos=0
        for i in val_temps:
            vp=self.ValuePicker(**i)
            self.Add(vp,(mypos,0),(1,1), wx.EXPAND,3)
            self.value_pickers.append(vp)
        self.add_final_spacer()
        self.Layout()

    class ValuePicker(wx.BoxSizer):
        def __init__(self,parent=None, value=None,clr=None, sz=2, checked=False, val_ctrl=None):
            self.c=controller.Controller()
            self.parent=parent
            self.value_picker_control=val_ctrl
            self.value=value
            self.clr=clr
            self.size=sz
            wx.BoxSizer.__init__(self,wx.HORIZONTAL)
            self.m_checkBox1 = wx.CheckBox(parent, wx.ID_ANY, value, wx.DefaultPosition, wx.DefaultSize, 0 )
            self.m_checkBox1.SetValue(checked)
            self.Add( self.m_checkBox1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

            self.m_colourPicker1 = wx.ColourPickerCtrl(parent, wx.ID_ANY, wx.Colour(clr[0],clr[1],clr[2]), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
            self.Add( self.m_colourPicker1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

            self.m_spinCtrl=wx.SpinCtrl(parent, initial=self.size)
            self.m_spinCtrl.SetMaxSize(wx.Size(50,-1))
            self.Add(self.m_spinCtrl,0,wx.ALL,5)

            self.m_spinCtrl.Bind(wx.EVT_SPINCTRL,self.process_size_change)

            self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.process_annotationvalue_check )
            self.m_colourPicker1.Bind( wx.EVT_COLOURPICKER_CHANGED, self.process_color_change )
            self.m_checkBox1.Bind(wx.EVT_LEFT_DCLICK,self.move_down_in_list)

        def move_down_in_list(self,event):
            fld=self.c.apm.node_annotation_level
            ind=self.c.apm.node_annotation.uniques[fld].index(self.value)
            # print self.c.apm.node_annotation.uniques[fld]
            self.c.apm.node_annotation.uniques[fld].pop(ind)
            self.c.apm.node_annotation.uniques[fld].append(self.value)
            # self.c.trigger_annotation_picker_refresh()

            self.value_picker_control.move_to_bottom(self.value)


        def process_annotationvalue_check(self,event=None):
            self.c.update_circles_by_annotation()
            self.c.trigger_refresh()

        def process_color_change(self,event):
            newcolor=self.m_colourPicker1.GetColour()
            self.clr=newcolor.Get()
            self.c.update_circles_by_annotation()
            self.c.trigger_refresh()

        def process_size_change(self,event):
            print "processing size change"
            self.size=int(self.m_spinCtrl.GetValue())
            self.c.update_circles_by_annotation()
            self.c.trigger_refresh()

sepp_otu_order = {'291658':1.1,
'New.ReferenceOTU3127':2.1,
'New.CleanUp.ReferenceOTU25':2.6,
'New.CleanUp.ReferenceOTU33':4.1,
'New.ReferenceOTU421':5.1,
'New.CleanUp.ReferenceOTU68':6.1,
'New.ReferenceOTU3100':7.1,
'New.ReferenceOTU2608':8.1,
'New.CleanUp.ReferenceOTU116':9.1,
'New.ReferenceOTU1350':10.1,
'New.ReferenceOTU608':11.1,
'New.CleanUp.ReferenceOTU110':12.1,
'New.CleanUp.ReferenceOTU127':13.1,
'New.ReferenceOTU425':14.1,
'New.ReferenceOTU760':15.1,
'197233':16.1,
'New.CleanUp.ReferenceOTU186':17.1,
'New.CleanUp.ReferenceOTU242':18.1,
'New.CleanUp.ReferenceOTU202':19.1,
'New.CleanUp.ReferenceOTU349':20.1,
'New.CleanUp.ReferenceOTU568':21.1,
'New.ReferenceOTU606':22.1,
'New.ReferenceOTU610':23.1,
'New.ReferenceOTU302':24.1,
'New.ReferenceOTU343':1.2,
'New.ReferenceOTU221':2.2,
'New.ReferenceOTU298':2.7,
'New.ReferenceOTU358':4.2,
'New.ReferenceOTU976':5.2,
'New.ReferenceOTU1154':6.2,
'New.ReferenceOTU750':7.2,
'New.ReferenceOTU1963':8.2,
'New.ReferenceOTU2511':9.2,
'New.ReferenceOTU1539':10.2,
'New.CleanUp.ReferenceOTU65':11.2,
'New.ReferenceOTU1351':12.2,
'New.ReferenceOTU1386':13.2,
'New.ReferenceOTU2512':14.2,
'New.ReferenceOTU3220':15.2,
'New.ReferenceOTU2377':16.2,
'New.ReferenceOTU219':17.2,
'New.ReferenceOTU1721':18.2,
'New.ReferenceOTU309':19.2,
'New.ReferenceOTU864':20.2,
'New.CleanUp.ReferenceOTU96':21.2,
'New.CleanUp.ReferenceOTU667':22.2,
'New.ReferenceOTU398':23.2,
'New.CleanUp.ReferenceOTU190':24.2,
'New.CleanUp.ReferenceOTU167':25.2,
'New.CleanUp.ReferenceOTU328':26.2,
'New.ReferenceOTU1177':27.2,
'New.CleanUp.ReferenceOTU579':28.2,
'New.CleanUp.ReferenceOTU464':29.2,
'New.CleanUp.ReferenceOTU304':30.2,
'New.ReferenceOTU1361':31.2,
'New.CleanUp.ReferenceOTU3513':32.2,
'New.CleanUp.ReferenceOTU7575':33.2,
'New.ReferenceOTU624':34.2,
'New.CleanUp.ReferenceOTU819':35.2,
'New.ReferenceOTU3':1.3,
'New.ReferenceOTU15':2.3,
'1145921':3.3,
'New.ReferenceOTU2':4.3,
'New.ReferenceOTU6':5.3,
'661055':6.3,
'317315':7.3,
'New.ReferenceOTU16':8.3,
'New.ReferenceOTU24':9.3,
'New.ReferenceOTU13':10.3,
'New.ReferenceOTU1841':11.3,
'New.ReferenceOTU42':12.3,
'New.ReferenceOTU36':13.3,
'New.ReferenceOTU74':14.3,
'New.ReferenceOTU30':15.3,
'New.ReferenceOTU57':16.3,
'New.ReferenceOTU271':17.3,
'New.ReferenceOTU247':18.3,
'New.ReferenceOTU106':19.3,
'237063':20.3,
'New.ReferenceOTU69':21.3,
'New.ReferenceOTU251':22.3,
'New.ReferenceOTU1837':23.3,
'207713':24.3,
'291202':25.3,
'New.ReferenceOTU193':26.3,
'New.ReferenceOTU133':27.3,
'New.ReferenceOTU465':28.3,
'New.ReferenceOTU104':29.3,
'New.ReferenceOTU218':30.3,
'New.ReferenceOTU363':31.3,
'New.ReferenceOTU153':32.3,
'New.ReferenceOTU163':33.3,
'110660':34.3,
'New.ReferenceOTU142':1.4,
'New.CleanUp.ReferenceOTU21':2.4,
'290338':3.4,
'300618':4.4,
'287909':5.4,
'New.ReferenceOTU3233':6.4,
'New.ReferenceOTU2947':7.4,
'215731':8.4,
'New.ReferenceOTU591':9.4,
'301818':10.4,
'New.ReferenceOTU839':11.4,
'4424113':12.4,
'New.CleanUp.ReferenceOTU157':13.4,
'New.ReferenceOTU613':14.4,
'New.ReferenceOTU707':15.4,
'239562':16.4,
'New.CleanUp.ReferenceOTU180':17.4,
'715152':18.4,
'New.CleanUp.ReferenceOTU174':19.4,
'New.ReferenceOTU2839':20.4,
'110016':21.4,
'619919':22.4}

sepp_otu_colors={
'291658':(0,255,0),
'New.ReferenceOTU3127':(255,0,0),
'New.CleanUp.ReferenceOTU25':(0,0,255),
'New.CleanUp.ReferenceOTU33':(255,255,0),
'New.ReferenceOTU421':(255,0,255),
'New.CleanUp.ReferenceOTU68':(0,255,255),
'New.ReferenceOTU3100':(0,100,1),
'New.ReferenceOTU2608':(255,128,0),
'New.CleanUp.ReferenceOTU116':(164,36,0),
'New.ReferenceOTU1350':(0,255,0),
'New.ReferenceOTU608':(255,0,0),
'New.CleanUp.ReferenceOTU110':(0,0,255),
'New.CleanUp.ReferenceOTU127':(255,255,0),
'New.ReferenceOTU425':(255,0,255),
'New.ReferenceOTU760':(0,255,255),
'197233':(0,100,1),
'New.CleanUp.ReferenceOTU186':(255,128,0),
'New.CleanUp.ReferenceOTU242':(164,36,0),
'New.CleanUp.ReferenceOTU202':(0,255,0),
'New.CleanUp.ReferenceOTU349':(255,0,0),
'1145921':(0,0,255),
'New.CleanUp.ReferenceOTU568':(255,255,0),
'New.ReferenceOTU606':(255,0,255),
'New.ReferenceOTU610':(0,255,255),
'New.ReferenceOTU302':(0,100,1),
'New.ReferenceOTU343':(255,128,0),
'New.ReferenceOTU221':(164,36,0),
'New.ReferenceOTU298':(0,255,0),
'New.ReferenceOTU358':(255,0,0),
'New.ReferenceOTU976':(0,0,255),
'New.ReferenceOTU1154':(255,255,0),
'New.ReferenceOTU750':(255,0,255),
'New.ReferenceOTU1963':(0,255,255),
'New.ReferenceOTU2511':(0,100,1),
'New.ReferenceOTU1539':(255,128,0),
'New.CleanUp.ReferenceOTU65':(164,36,0),
'New.ReferenceOTU1351':(0,255,0),
'New.ReferenceOTU1386':(255,0,0),
'New.ReferenceOTU2512':(0,0,255),
'New.ReferenceOTU3220':(255,255,0),
'New.ReferenceOTU2377':(255,0,255),
'290338':(0,255,255),
'New.ReferenceOTU219':(0,100,1),
'New.ReferenceOTU1721':(255,128,0),
'New.ReferenceOTU309':(164,36,0),
'New.ReferenceOTU864':(0,255,0),
'New.CleanUp.ReferenceOTU96':(255,0,0),
'New.CleanUp.ReferenceOTU667':(0,0,255),
'New.ReferenceOTU398':(255,255,0),
'New.CleanUp.ReferenceOTU190':(255,0,255),
'New.CleanUp.ReferenceOTU167':(0,255,255),
'New.CleanUp.ReferenceOTU328':(0,100,1),
'New.ReferenceOTU1177':(255,128,0),
'New.CleanUp.ReferenceOTU579':(164,36,0),
'New.CleanUp.ReferenceOTU464':(0,255,0),
'New.CleanUp.ReferenceOTU304':(255,0,0),
'New.ReferenceOTU1361':(0,0,255),
'New.CleanUp.ReferenceOTU3513':(255,255,0),
'New.CleanUp.ReferenceOTU7575':(255,0,255),
'New.ReferenceOTU624':(0,255,255),
'New.CleanUp.ReferenceOTU819':(0,100,1),
'New.ReferenceOTU3':(255,128,0),
'New.ReferenceOTU15':(164,36,0),
'1145921':(0,255,0),
'New.ReferenceOTU2':(255,0,0),
'New.ReferenceOTU6':(0,0,255),
'661055':(255,255,0),
'317315':(255,0,255),
'New.ReferenceOTU16':(0,255,255),
'New.ReferenceOTU24':(0,100,1),
'New.ReferenceOTU13':(255,128,0),
'New.ReferenceOTU1841':(164,36,0),
'New.ReferenceOTU42':(0,255,0),
'New.ReferenceOTU36':(255,0,0),
'New.ReferenceOTU74':(0,0,255),
'New.ReferenceOTU30':(255,255,0),
'New.ReferenceOTU57':(255,0,255),
'New.ReferenceOTU271':(0,255,255),
'New.ReferenceOTU247':(0,100,1),
'New.ReferenceOTU106':(255,128,0),
'237063':(164,36,0),
'New.ReferenceOTU69':(0,255,0),
'New.ReferenceOTU251':(255,0,0),
'New.ReferenceOTU1837':(0,0,255),
'207713':(255,255,0),
'291202':(255,0,255),
'New.ReferenceOTU193':(0,255,255),
'New.ReferenceOTU133':(0,100,1),
'New.ReferenceOTU465':(255,128,0),
'New.ReferenceOTU104':(164,36,0),
'New.ReferenceOTU218':(0,255,0),
'New.ReferenceOTU363':(255,0,0),
'New.ReferenceOTU153':(0,0,255),
'New.ReferenceOTU163':(255,255,0),
'110660':(255,0,255),
'New.ReferenceOTU142':(0,255,255),
'New.CleanUp.ReferenceOTU21':(0,100,1),
'290338':(255,128,0),
'300618':(164,36,0),
'287909':(0,255,0),
'New.ReferenceOTU3233':(255,0,0),
'New.ReferenceOTU2947':(0,0,255),
'215731':(255,255,0),
'New.ReferenceOTU591':(255,0,255),
'301818':(0,255,255),
'New.ReferenceOTU839':(0,100,1),
'4424113':(255,128,0),
'New.CleanUp.ReferenceOTU157':(164,36,0),
'New.ReferenceOTU613':(0,255,0),
'New.ReferenceOTU707':(255,0,0),
'239562':(0,0,255),
'New.CleanUp.ReferenceOTU180':(255,255,0),
'715152':(255,0,255),
'New.CleanUp.ReferenceOTU174':(0,255,255),
'New.ReferenceOTU2839':(0,100,1),
'110016':(255,128,0),
'619919':(164,36,0)
}

clostridiales_familiy_colors={
'Clostridiaceae':{'color':(0,255,0),'order':1.1},
'Lachnospiraceae':{'color':(0,0,255),'order':2.1},
'Peptococcaceae':{'color':(255,0,0),'order':3.1},
'Ruminococcaceae':{'color':(1,255,254),'order':4.1},
'Eubacteriaceae':{'color':(255,166,254),'order':5.1},
'Clostridiales Family XI. Incertae Sedis':{'color':(255,219,102),'order':6.1},
'Peptostreptococcaceae':{'color':(0,100,1),'order':7.1},
'Syntrophomonadaceae':{'color':(1,0,103),'order':8.1},
'#N/A':{'color':(149,0,58),'order':9.1},
'Clostridiales Family XIII. Incertae Sedis':{'color':(0,0,0),'order':10.1},
'Clostridiales Family XVII. Incertae Sedis':{'color':(0,0,0),'order':11.1},
'Heliobacteriaceae':{'color':(0,125,181),'order':12.1},
'Clostridiales Family XII. Incertae Sedis':{'color':(0,0,0),'order':13.1},
'Proteinivoraceae':{'color':(255,0,246),'order':14.1},
'Caldicoprobacteraceae':{'color':(255,238,232),'order':15.1},
'Clostridiales Family XIX. Incertae Sedis':{'color':(0,0,0),'order':16.1},
'Clostridiales Family XVI. Incertae Sedis':{'color':(0,0,0),'order':17.1},
'Clostridiales Family XVIII. Incertae Sedis':{'color':(0,0,0),'order':18.1},
'Defluviitaleaceae':{'color':(119,77,0),'order':19.1},
'Gracilibacteraceae':{'color':(144,251,146),'order':20.1},
'Oscillospiraceae':{'color':(0,118,255),'order':21.1},
'clostridiaceae_1':{'color':(0,255,0),'order':1.2},
'lachnospiraceae':{'color':(0,0,255),'order':2.2},
'veillonellaceae':{'color':(126,45,210),'order':3.2},
'ruminococcaceae':{'color':(1,255,254),'order':4.2},
'peptococcaceae_2':{'color':(255,0,0),'order':5.2},
'peptostreptococcaceae':{'color':(0,100,1),'order':6.2},
'peptococcaceae_1':{'color':(255,0,0),'order':7.2},
'clostridiales_incertae_sedis_xi':{'color':(0,0,0),'order':8.2},
'eubacteriaceae':{'color':(255,166,254),'order':9.2},
'clostridiales_incertae_sedis_iii':{'color':(0,0,0),'order':10.2},
'syntrophomonadaceae':{'color':(1,0,103),'order':11.2},
'clostridiaceae_2':{'color':(0,255,0),'order':12.2},
'clostridiales_incertae_sedis_xviii':{'color':(0,0,0),'order':13.2},
'clostridiales_incertae_sedis_xvii':{'color':(0,0,0),'order':14.2},
'heliobacteriaceae':{'color':(0,125,181),'order':15.2},
'incertae_sedis_xi':{'color':(0,0,0),'order':16.2},
'clostridiales_incertae_sedis_xiii':{'color':(0,0,0),'order':17.2},
'clostridiaceae_3':{'color':(0,255,0),'order':18.2},
'clostridiales_incertae_sedis_xii':{'color':(0,0,0),'order':19.2},
'clostridiales_incertae_sedis_xiv':{'color':(0,0,0),'order':20.2},
'clostridiaceae_4':{'color':(0,255,0),'order':21.2},
'gracilibacteraceae':{'color':(144,251,146),'order':22.2},
'incertae_sedis_iii':{'color':(0,0,0),'order':23.2},
'clostridiales_incertae_sedis':{'color':(0,0,0),'order':24.2},
'clostridiales_incertae_sedis_iv':{'color':(0,0,0),'order':25.2},
'clostridiales_incertae_sedis_xvi':{'color':(254,137,0),'order':26.2},
'incertae_sedis_iv':{'color':(0,0,0),'order':27.2},
'peptococcaceae_i':{'color':(255,0,0),'order':28.2},
}

if __name__=='__main__':
    unit_test_line_on_screen()