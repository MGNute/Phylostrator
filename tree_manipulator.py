__author__ = 'Michael'

import math
import dendropy
from view import *
from utilities import *
import copy
import wx
import numpy as np
import scipy.spatial as spat
import sys
import datetime, time

GLOBAL_DEBUG = True

# class Singleton(type):
#     def __init__(cls, name, bases, dict):
#         super(Singleton, cls).__init__(name, bases, dict)
#         cls.instance = None
#
#     def __call__(cls, *args, **kw):
#         if not cls.instance:
#             # Not created or has been Destroyed
#             obj = super(Singleton, cls).__call__(*args, **kw)
#             cls.instance = obj
#         return cls.instance

class AnnotatedPhylogramModel():
    tree_file = None
    annotation_file = None

    def __init__(self):
        #state information
        self.state_tree_loaded=False
        self.state_node_annotation_loaded=False
        self.rp = None

        #picture information
        self.node_annotation = None
        self.segments=[]
        self.node_coordinates={}
        self.node_annotation_level=None
        self.checked=[]

    def initialize_tree(self,tp=None):

        if tp<> None:
            self.tree_file=tp
        self.rp=Radial_Phylogram(self.tree_file)
        self.rp.get_segments()
        self.segments=self.rp.segments
        self.state_tree_loaded=True

    def unload_tree(self):
        self.rp=None
        self.rp.segments=[]
        self.state_tree_loaded=False

    def initialize_annotation(self,ann_path):
        self.annotation_file=ann_path
        self.node_annotation=SfldAnnotationData(self.annotation_file)
        self.state_node_annotation_loaded=True


    pass

class Radial_Phylogram():
    '''
    Right now it requires the tree to have labels equal to the "efd_id" field from the node_annotation
    '''
    max_dims = None
    myt_copy = None


    def __init__(self,tp=None):
        self.treepath=''
        self.myt=None
        self.node_labels={}
        self.segments=[]
        self.selected=[]
        self.leaf_node_coords={}
        self.selected_color=None
        self.rotation=0
        if tp is not None:
            self.set_treepath(tp)
        # self.print_right_angles()

    # def set_rotation(self,rotation):
    #     '''
    #
    #     :param rotation: rotation given in degrees
    #     :return:
    #     '''
    #     self.rotation=rotation/360 * 2 * math.pi
    #     tp = self.treepath
    #     self.set_treepath(tp)
        # self.get_radial_phylogram()
        # self.get_segments()
        # self.get_max_dims()

    def spacefill_get_space_filling_phylogram(self):
        '''
        This function will populate the dendropy tree with a set of properties on each edge and node that
        define a 2D tree layout that approximately fills the rectangular viewing area optimally.

        The properties are:
        'deflect_angle' on each edge,
        'location' on each node and an
        'aspect_ratio'on the tree object.

        The layout is defined by a root-edge, the aspect ratio and the deflect angles (
        positive = clockwise). Default aspect ratio is 1.6 (w/h)
        :return:
        '''
        if self.myt.aspect_ratio is None:
            self.myt.aspect_ratio = 1.6
        to = 0
        for i in self.myt.postorder_edge_iter():
            if i.length is None:
                i.length = 0.0
            to += i.length

        self.myt.calc_node_ages(ultrametricity_precision=False,is_force_max_age=True)
        self.myt.calc_node_root_distances(False)

        first = True
        for i in self.myt.postorder_edge_iter():
            current_opposite_dist=0
            if first==True:
                root_childs= i.head_node.child_nodes()
                root_child_dists = [(j.age+j.edge_length) for j in root_childs]
                root_opposite_dists = [(max(root_child_dists[:ind]+root_child_dists[(ind+1):])) for ind in range(len(root_childs))]
                first = False
            else:
                if i.head_node in root_childs:
                    ind = root_childs.index(i)
                    current_opposite_dist = root_opposite_dists[ind]

            if i.head_node.is_leaf() == True:
                i.head_mass = 0
                i.tail_mass = to - i.length
                # i.head_width = -1
                i.head_len = i.length
                i.tail_len = i.head_node.parent.root_distance + current_opposite_dist
                # i.tail_width =
            else:
                cn = i.head_node.child_nodes()
                i.head_mass = sum([(k.edge.head_mass + k.edge.length) for k in cn])
                i.tail_mass = to - i.length - i.head_mass
                i.head_len = i.length+i.age
                i.tail_len = i.head_node.parent.root_distance + current_opposite_dist

        self.cent_edge = self.spacefill_get_centroid_edge()
        self.cent_child_nodes = []
        for e in self.cent_edge.adjacent_edges:
            if e.head_node==self.cent_edge.head_node:
                self.cent_child_nodes.append(e.tail_node)
            else:
                self.cent_child_nodes.append(e.head_node)

        self.myt.reroot_at_edge(self.cent_edge)
        for i in self.myt.preorder_node_iter():
            if i.length is None:
                i.length = 0.

        self.myt.calc_node_ages(ultrametricity_precision=False,is_force_max_age=True)
        self.myt.calc_node_root_distances(False)

        d = self.cent_edge.length

        for i in self.cent_child_nodes:
            ages=[(j.age + j.edge_length) for j in i.child_nodes()]
            # TODO: continue here

    def spacefill_get_centroid_edge(self):
        '''
        finds the edge with the minimal squared deviation from a (1/4, 1/4, 1/4, 1/4) split based
        on the 'age' attribute of the four child nodes (plus lengths)
        :return:
        '''
        m_sse = 9999999.0
        cent_edge = None
        for i in self.myt.preorder_edge_iter():
            eds = i.adjacent_edges
            hn = i.head_node
            tn = i.tail_node
            if len(eds)>=4:
                heads= [(e.head_node==hn or e.head_node==tn) for e in eds]
                k = len(heads)
                lens = [0.]*k
                for ind in range(k):
                    if heads[ind]==True:
                        lens[ind]=eds[ind].length+eds[ind].tail_len
                    else:
                        lens[ind]=eds[ind].length+eds[ind].head_len
                all_lens = sum(lens)
                sse=sum([(j/all_lens-1.0/float(k))**2 for j in lens])
                if sse < m_sse:
                    m_sse = sse
                    cent_edge = i
        return cent_edge

    def dump_all(self):
        del self.myt
        self.myt=None
        del self.segments
        self.segments=None

    def set_treepath(self,tp):
        self.treepath=tp
        self.myt=dendropy.Tree.get(file=open(self.treepath,'r'),schema="newick",preserve_underscores=True)
        self.get_radial_phylogram()
        self.get_max_dims()
        self.get_leaf_node_coords()
        self.get_segments()
        self.myt.m_matrix = None
        print 'Successfully imported tree. Number of Taxa: %s' % len(self.myt.leaf_nodes())


    def get_radial_phylogram(self):
        # myt=set_treepath(tp)
        # theta_vals=[]
        # theta_vals2=[]
        # theta_vals3=[]

        self.node_ct = 0
        self.prepare_tree()
        for i in self.myt.postorder_node_iter():
            self.node_ct +=1
            if i.is_leaf()==True:
                self.node_labels[i.label]['l']=1
            else:
                child_l=0
                for j in i.child_node_iter():
                    child_l+=self.node_labels[j.label]['l']
                self.node_labels[i.label]['l']=child_l
        pr=self.myt.preorder_node_iter()
        r=pr.next()

        self.node_labels[r.label]['x']=(0.0,0.0)
        r.location = (0.0,0.0)
        r.deflect_angle = 0.
        r.wedge_angle = 2*math.pi
        r.edge_segment_angle = 0.
        r.right_wedge_border = 0.
        self.node_labels[r.label]['w']=2*math.pi
        self.node_labels[r.label]['t']=0.0
        self.node_labels[r.label]['nu']=0.0
        leafct=len(r.leaf_nodes())

        # k=0
        for i in pr:
            # k+=1
            # print k
            # if i.edge_length is None:
            # i.edge_length = 0.001 # debug
            ww=float(len(i.leaf_nodes()))/leafct*2*math.pi
            self.node_labels[i.label]['w']=ww   # wedge angle
            i.wedge_angle=ww
            i.right_wedge_border =self.node_labels[i.parent_node.label]['nu']
            self.node_labels[i.label]['t']=i.right_wedge_border # angle of right wedge border
            # theta_vals.append(self.node_labels[i.label]['t'])
            self.node_labels[i.label]['nu']=self.node_labels[i.label]['t']
            thetav=self.node_labels[i.parent_node.label]['nu']+ww/2
            i.edge_segment_angle=thetav
            self.node_labels[i.label]['theta']=thetav
            # theta_vals2.append(i.label)
            self.node_labels[i.parent_node.label]['nu']+=ww
            xu=self.node_labels[i.parent_node.label]['x']
            delta=i.edge_length
            try:
                x1=xu[0]+delta*math.cos(thetav)
                x2=xu[1]+delta*math.sin(thetav)
            except:
                print 'thetav is %d' % thetav
                x1=xu[0]
                x2=xu[1]
            i.location = (x1,x2)
            i.deflect_angle = thetav - self.node_labels[i.parent_node.label]['theta']
            # theta_vals3.append(self.node_labels[i.label]['t'])
            # x1_orig = xu[0] + delta * math.cos(thetav)
            # x2_orig = xu[1] + delta * math.sin(thetav)
            # x1 = x1_orig*math.cos(self.rotation)-x2_orig*math.sin(self.rotation)
            # x2 = x1_orig*math.sin(self.rotation)+x2_orig*math.cos(self.rotation)
            self.node_labels[i.label]['x']=(x1,x2)

        for i in self.myt.preorder_internal_node_iter():
            w = i.wedge_angle
            for j in i.child_node_iter():
                j.percent_of_parent_wedge=j.wedge_angle/w

        ct = 0
        self.pts_nparr = np.zeros((self.node_ct,2),dtype=np.float64)
        eip = []
        for i in self.myt.preorder_node_iter():
            i.index = ct
            self.pts_nparr[i.index,:]=i.location
            if i.parent_node is not None:
                eip.append((i.index,i.parent_node.index))
            ct +=1
        self.edges_as_node_pairs = np.asarray(eip,dtype=np.int32)
        # print self.edges_as_node_pairs.shape

    def make_tree_copy(self,parent, evt):
        # if self.myt_copy is not None:
        #     del self.myt_copy
        # self.myt_copy=copy.deepcopy(self.myt)
        print 'event set in make_tree_copy'
        evt.set()
        # wx.CallAfter(parent.UpdateDrawing)

    def relocate_subtree_by_deflect_angle(self,node):
        '''
        runs a preorder node iteration and uses the current deflection angles of each node to replace
        its current location with a new location.
        :param node:
        :return:
        '''
        for i in node.preorder_iter():
            t0 = i.parent_node.edge_segment_angle
            x0 = i.parent_node.location
            t1 = i.deflect_angle + t0
            x1x = x0[0]+i.edge_length*math.cos(t1)
            x1y = x0[1]+i.edge_length*math.sin(t1)
            i.location = (x1x,x1y)
            self.pts_nparr[i.index, :] = i.location

    def relocate_subtree_by_edge_segment_angle(self,node=None):
        '''
        runs a preorder node iteration and uses the current deflection angles of each node to replace
        its current location with a new location.
        :param node:
        :return:
        '''
        if node <> None:
            for i in node.preorder_iter():
                x0 = i.parent_node.location
                t1 = i.edge_segment_angle
                x1x = x0[0]+i.edge_length*math.cos(t1)
                x1y = x0[1]+i.edge_length*math.sin(t1)
                i.location = (x1x,x1y)
                self.pts_nparr[i.index,:]= i.location
        else:
            pr = self.myt.preorder_node_iter()
            pr.next()
            for i in pr:
                x0 = i.parent_node.location
                t1 = i.edge_segment_angle
                x1x = x0[0]+i.edge_length*math.cos(t1)
                x1y = x0[1]+i.edge_length*math.sin(t1)
                i.location = (x1x,x1y)
                self.pts_nparr[i.index, :] = i.location

    def spacefill_spread_tree_by_levelorder(self, parent):
        '''
        do a level-order node iteration over the (non-root) leaves. At each one, calculate the
        de facto spread angle and compare it to the allowable. Boost the allowable by up to 25%.
        :return:
        '''
        levelo=self.myt.levelorder_node_iter()
        rt = levelo.next()

        ct = 0
        max_ct = 30
        for i in levelo:
            df_min_max = self.get_de_facto_spread_angle(i)
            df_spread = df_min_max[1]-df_min_max[0]
            if df_spread < .8*i.wedge_angle:
                for j in i.child_nodes():
                    j.percent_of_parent_wedge*=1.25
                self.relocate_subtree_by_wedge_properties(i)
                ct +=1
                print "done with %s expansions" % ct
                if ct % 50 == 0:
                    self.make_tree_copy(parent)
                    # print 'press any key to continue'
                    # raw_input()
                    # parent.UpdateDrawing()
            else:
                print "wedge angle x .9: %s, de-facto spread: %s" % (.9*i.wedge_angle,df_spread)
            # if ct >=max_ct:
            #     break
        print "done with spacefill by levelorder"

    def test_1(self):
        for i in self.myt.preorder_node_iter():
            if i.label == 'label11':
                test_nd = i
                break

        print '---------test 1: label11 -------------------------------'
        print test_nd.__dict__
        dfs = self.get_de_facto_spread_angle(test_nd)
        print 'min %.4f -- max %.4f -- spread %.4f' % (dfs[0],dfs[1],dfs[1]-dfs[0])

    def test_2(self):
        for i in self.myt.preorder_node_iter():
            if i.label == 'label11':
                test_nd = i
                break

        for j in test_nd.child_nodes():
            j.percent_of_parent_wedge*=1.0
        self.relocate_subtree_by_wedge_properties(test_nd)

    def test_3(self):
        self.set_segments_as_nparr()
        print np_find_intersect_segments_test(self.segments_as_nparr)
        pass

    def test_4(self, parent=None, myevt = None):
        '''
        delauny triangulation method
        :return:
        '''
        ndct, node_order, pts, pts_leaves_bln, tri, pts_nparr = self.get_delaunay_trianglization()


        # declare some matrices for the partials

        ''' M here has a specific definition. A column of M represents a node somewhere on the tree,
        and the columsn are indexed by the node labels. The rows of M are indexed by branches (equivalently,
        also nodes). The (i,j)-th entry of M (row i, col j) is 1 iff branch i is on the path from the root
        to node j.
        '''
        # M = np.zeros((ndct, lct), dtype=np.float64)  # for K leaves, M is [(2K-2) X K]
        # using all delaunay distances, not just leaves:
        M = np.zeros((ndct, ndct), dtype=np.float64)  # for K leaves, M is [(2K-2) X (2K-2)]

        lens = np.zeros(ndct, dtype=np.float64)
        thetas = np.zeros(ndct, dtype=np.float64)

        # Make the 'M' matrix:
        if GLOBAL_DEBUG==True:
            print 'making the M matrix'
        do_M = (self.myt.m_matrix is None)
        pr = self.myt.preorder_node_iter()
        pr.next() #(excluding the first one)
        for nd in pr:
            nd_ind = pts[nd.label]['index']
            t_i = nd.edge_segment_angle
            thetas[nd_ind] = t_i

            L_i = nd.edge_length
            lens[nd_ind] = L_i

            if do_M == True:

                for sub_nd in nd.preorder_iter():
                    sub_nd_ind = pts[sub_nd.label]['index']
                    M[nd_ind,sub_nd_ind]=1.
            else:
                M = self.myt.m_matrix
        if do_M==True:
            # storing the M matrix and the pts object in the tree for later.
            self.myt.m_matrix=M

        # np.savetxt('C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\phylostrator-testing\\test-M.txt', M, '%.2f', '\t')

        if GLOBAL_DEBUG == True:
            print 'getting delaunay leaf segments'
        seg_inds = self.get_delaunay_leaf_segments( pts_leaves_bln,  tri)
        leaf_to_edge_segs = self.get_delaunay_leaf_to_edge_segments(tri,pts_nparr)

        # get the gradient vector
        if GLOBAL_DEBUG == True:
            print 'getting the gradient vector'
        gradients = self.get_delaunay_gradients(M, lens, node_order, pts, seg_inds,
                                                thetas, ndct, pts_nparr, leaf_to_edge_segs)
        # np.savetxt('C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\phylostrator-testing\\test-gradients.txt', gradients,
        #            '%.2f', '\t')
        if GLOBAL_DEBUG == True:
            print 'done with delaunay gradients'

        loss = self.get_total_loss(pts_nparr, seg_inds)
        print 'Starting Loss: %s' % loss

        step = .01
        # max_angle_change = np.pi / (float(ndct)/2.)
        max_angle_change = .017*10
        self.po_ct = 0

        ok_to_continue = True
        q=None

        # trying the all at once method:
        eff_grads = np.dot(2*np.identity(ndct,dtype=np.float64)-M.transpose(),gradients)
        np.savetxt('C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\phylostrator-testing\\test-effgrads.txt',eff_grads,'%.2f', '\t')

        # ct +=0
        for i in self.myt.preorder_node_iter():
            last_edge_angles = self.get_tree_restore_point(ndct)
            i.edge_segment_angle += min(max(-max_angle_change, step * gradients[i.index]), max_angle_change)
            self.relocate_subtree_by_edge_segment_angle()
            self.set_segments_as_nparr()
            if np_find_intersect_segments(self.segments_as_nparr) == False:
                print "breaking because we found an intersection"
                print np_find_intersect_segments_allpy(self.segments_as_nparr)
                self.set_tree_to_last_restore_point(last_edge_angles)
                break


            # print 'index: %s -- gradient %s -- angle change %s' % (i.index, gradients[i.index],min(max(-max_angle_change, step * gradients[i.index]), max_angle_change))
            myevt.set()
            # time.sleep(0.1)

            q=raw_input()
            if q == 'q':
                break
        self.relocate_subtree_by_edge_segment_angle()
        # self.make_tree_copy(parent,myevt)

        # while (self.po_ct < 30):
        #     ct = 0
        #     last_edge_angles=self.get_tree_restore_point(ndct)
        #     all_segs = np.zeros((ndct,4),dtype=np.float64)
        #     # for i in self.myt.postorder_node_iter():
        #     for i in self.myt.levelorder_node_iter():
        #         i.edge_segment_angle += min(max(-max_angle_change,step * gradients[i.index]),max_angle_change)
        #
        #         ct +=1
        #         if ct % 1 ==0:
        #             self.make_tree_copy(parent,myevt)
        #             tic=datetime.datetime.now()
        #             # gradients, loss = self.refresh_and_redraw(M, lens, ndct, node_order, parent,
        #             #                                           pts, pts_nparr, seg_inds, thetas, new_delaunay=True, pts_leaves_bln=pts_leaves_bln)
        #             self.relocate_subtree_by_edge_segment_angle()
        #             self.update_pts_np_array(pts_nparr)
        #
        #             # check for intersections
        #             pr = self.myt.preorder_node_iter()
        #             pr.next()
        #             for i in pr:
        #                 all_segs[i.index, 0:2] = i.location
        #                 all_segs[i.index, 2:4] = i.parent_node.location
        #             check_intersect = np_find_intersect_segments(all_segs)
        #             ok_to_continue = check_intersect[0]
        #             if ok_to_continue == True:
        #                 print 'No intersections found, continuing for another round'
        #                 last_edge_angles = self.get_tree_restore_point(ndct)
        #             else:
        #                 # parent.draw_red_line_pair(check_intersect[1],check_intersect[2])
        #                 # parent.UpdateDrawing()
        #                 self.set_tree_to_last_restore_point(last_edge_angles)
        #                 print 'Intersection found, resetting to last restore point'
        #                 print check_intersect
        #             toc = datetime.datetime.now()
        #             print 'Finished with all steps after %s nodes in %s seconds.' % (ct, toc-tic)
        #         if ct % 25 == 0:
        #             print 'ct = %s' % ct
        #             gradients, loss = self.refresh_and_redraw(M, lens, ndct, node_order, parent,
        #                                                       pts, pts_nparr, seg_inds, thetas,
        #                                                       new_delaunay=True, pts_leaves_bln=pts_leaves_bln)
        #     self.po_ct += 1
        #     print 'Done with one full postorder edit. Total loss = %s' % self.get_total_loss(pts_nparr, seg_inds)




            # if po_ct % 2 ==0:
            #     q=raw_input()
            #     if q=='q':
            #         # np.savetxt('C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\phylostrator-testing\\all_segs.txt',all_segs,delimiter='\t')
            #         break
        # self.set_tree_to_last_restore_point(last_edge_angles)
        # self.make_tree_copy(parent)


        # levelorder_hash = self.get_levelorder_hash()
        # levels = levelorder_hash.keys()
        #
        # levels.sort(reverse=True)
        # for level in levels:
        #     if GLOBAL_DEBUG == True:
        #         print 'starting level %s' % level
        #     angle_changes = []
        #     for i in levelorder_hash[level]:
        #         # ind = pts[i.label]['index']
        #         i.edge_segment_angle += step * gradients[i.index]
        #         angle_changes.append(step * gradients[i.index])
        #     if len(angle_changes)>30:
        #         angle_changes = angle_changes[0:30]
        #     print 'angle changes: %s' % map(lambda x: '%.3f' % x, angle_changes)
        #
        #     gradients, loss = self.refresh_and_redraw(M, gradients, lens, loss, ndct, node_order, parent, pts,
        #                                               pts_nparr, seg_inds, thetas)
        #     if GLOBAL_DEBUG==True:
        #     #     # print 'done with callback, setting status.'
        #         print 'Level %s\tLoss: %s\n' % (level, loss)
        #
        #         # print 'status should say: Done with level %s, press a key to continue (q to exit thread)' % level
        #     # parent.parent.set_status('Done with level %s, press a key to continue' % level)
        #     cmd=raw_input()
        #     if cmd=='q':
        #         print 'exiting space fill function'
        #         return
        loss = self.get_total_loss(pts_nparr, seg_inds)
        print 'Loss after full iteration: %s' % loss
        parent.parent.set_status('Ready')
        print 'exiting space fill function'

    def set_segments_as_nparr(self):
        edge_ct = self.edges_as_node_pairs.shape[0]
        self.segments_as_nparr = np.zeros((edge_ct,4),dtype=np.float64)
        self.segments_as_nparr[:, 0:2] = self.pts_nparr[self.edges_as_node_pairs[:, 0],:]
        self.segments_as_nparr[:, 2:4] = self.pts_nparr[self.edges_as_node_pairs[:, 1],:]

    def fix_missing_edge_lengths(self):
        lens = []
        pr = self.myt.preorder_node_iter()
        pr.next()
        for i in pr:
            if i.edge.length is not None:
                i.edge.orig_edge_length = i.edge.length
                lens.append(i.edge.length)
            else:
                i.edge.orig_edge_length = None
        mean_len = np.mean(np.asarray(lens,dtype=np.float64))
        pr = self.myt.preorder_node_iter()
        pr.next()
        pr.next()
        for i in pr:
            if i.edge.length is None or i.edge.length==0:
                i.edge.length = mean_len

        # leaflens=[]
        # for i in self.myt.leaf_node_iter():
        #     leaflens.append(i.edge_length)
        # print leaflens



    def get_tree_restore_point(self, ndct):
        last_edge_angles = np.zeros(ndct,dtype=np.float64)
        pr = self.myt.preorder_node_iter()
        pr.next()
        for i in pr:
            last_edge_angles[i.index]=i.edge_segment_angle
        return last_edge_angles

    def set_tree_to_last_restore_point(self,last_edge_angles):
        pr = self.myt.preorder_node_iter()
        pr.next()
        for i in pr:
            i.edge_segment_angle = last_edge_angles[i.index]
        self.relocate_subtree_by_edge_segment_angle()

    def refresh_and_redraw(self, M,  lens, ndct, node_order, parent, pts, pts_nparr, seg_inds, thetas, full_redraw=False, new_delaunay=False, pts_leaves_bln=None):
        self.relocate_subtree_by_edge_segment_angle()
        # print full_redraw
        # if full_redraw:
        #     self.make_tree_copy(parent)
        self.update_pts_np_array(pts_nparr)

        leaf_to_edge_segs = None
        if new_delaunay==True:
            tri = spat.Delaunay(pts_nparr)
            seg_inds=self.get_delaunay_leaf_segments(pts_leaves_bln,tri)
            leaf_to_edge_segs=self.get_delaunay_leaf_to_edge_segments(tri,pts_nparr)
        gradients = self.get_delaunay_gradients(M, lens, node_order, pts, seg_inds,
                                                thetas, ndct, pts_nparr, leaf_to_edge_segs)
        loss = self.get_total_loss(pts_nparr, seg_inds)
        return gradients, loss

    def update_pts_np_array(self,pts_nparr):
        tic = datetime.datetime.now()
        pr = self.myt.preorder_node_iter()
        pr.next()
        for i in pr:
            pts_nparr[i.index,:]=i.location
            self.pts_nparr[i.index,:]=i.location
        toc = datetime.datetime.now()
        # print 'Points numpy array updated. Time: %s' % (toc - tic)

    def get_levelorder_hash(self):
        '''
        returns a dictionary object indexed by level (integers) and containing a list of references to node
        objects at that level. Excludes the root of the tree.
        '''
        lo = self.myt.levelorder_node_iter()
        a=lo.next()
        l_hash={}
        for i in lo:
            l = i.level()
            if l not in l_hash.keys():
                l_hash[l]=[]
            l_hash[l].append(i)
        return l_hash

    def get_total_loss(self,pts_nparr,seg_inds):
        s1 = pts_nparr[seg_inds[:, 0]]
        s2 = pts_nparr[seg_inds[:, 1]]
        return np.sum(np.sqrt(np.sum((s1-s2)**2,1)), 0)

    def get_delaunay_gradients(self, M, lens, node_order, pts, seg_inds, thetas, ndct, pts_nparr, leaf_to_edge_segs=None):

        tic = datetime.datetime.now()
        dLdx = np.zeros(ndct, dtype=np.float64)
        dLdy = np.zeros(ndct, dtype=np.float64)

        nsegs = seg_inds.shape[0]

        s1 = pts_nparr[seg_inds[:,0]]
        s2 = pts_nparr[seg_inds[:,1]]
        sq_norms = np.sum((s1-s2)**2,1)
        dLdx_pre = (s1-s2).transpose()/sq_norms
        total_loss = np.sum(np.sqrt(sq_norms),0)

        # TODO: take care of the double counting in this:
        for i in range(nsegs):
            dLdx[seg_inds[i, 0]] += dLdx_pre[0,i]
            dLdx[seg_inds[i, 1]] += -dLdx_pre[0,i]

            # #DEBUG
            # if seg_inds[i,0]==test_nd_ind:
            #     opp_node=self.node_refs[seg_inds[i,1]]
            #     debug_file.write('Node\t' + opp_node.label + '\t' + str(dLdx_pre[0,i]) + '\t' + str(dLdx_pre[1,i]) + '\t' + str(sq_norms[i]) + '\n')
            # elif seg_inds[i,1]==test_nd_ind:
            #     opp_node=self.node_refs[seg_inds[i,0]]
            #     debug_file.write('Node\t' + opp_node.label + '\t' + str(-dLdx_pre[0, i]) + '\t' + str(-dLdx_pre[1, i]) + '\t' + str(sq_norms[i]) + '\n')
        # if GLOBAL_DEBUG == True:
        #     print 'running through second O(n) loop in gradients function...'
        for i in range(nsegs):
            dLdy[seg_inds[i, 0]] += dLdx_pre[1,i]
            dLdy[seg_inds[i, 1]] += -dLdx_pre[1,i]

        # add in the impacts of the distances to other edges in the delaunay:
        if leaf_to_edge_segs is not None:
            for i in leaf_to_edge_segs:
                lds = np.hstack((pts_nparr[i[0],:], pts_nparr[i[1],:], pts_nparr[i[2],:])) # points of the triangle: (tipp, hypot[1], hypot[2])
                denom = lds[0]*(lds[5]-lds[3])-lds[1]*(lds[4]-lds[2])+lds[4]*lds[3]-lds[5]*lds[2]
                if np.abs(denom) > .0000000001:
                    dLdx[i[0]] +=  np.sign(denom)*(lds[5]-lds[3])/np.abs(denom)
                    dLdy[i[0]] += -np.sign(denom) * (lds[4] - lds[2]) / np.abs(denom)

                # DEBUG
                # if i[0]==test_nd_ind:
                #     opplab = self.node_refs[i[1]].label + '-to-' + self.node_refs[i[2]].label
                #     debug_file.write('Edge\t' + opplab + '\t' + str(np.sign(denom)*(lds[5]-lds[3])/np.abs(denom))
                #                      + '\t' + str(-np.sign(denom) * (lds[4] - lds[2]) / np.abs(denom)) + '\t'
                #                      + str(np.abs(denom) / np.linalg.norm(lds[2:4]-lds[4:6])) + '\n')

        # finally, the distances to sibling edges:
        pr = self.myt.preorder_node_iter()
        pr.next()
        for i in pr:
            sn = i.sibling_nodes()
            if len(sn)>0:
                for j in sn:
                    tipp = pts_nparr[i.index,:]
                    h0 = pts_nparr[j.index,:]
                    h1 = pts_nparr[j.parent_node.index,:]
                    lds = np.hstack((tipp,h0,h1))

                    i_node = (i.index, j.index, j.parent_node.index)
                    if np.linalg.norm(h1-h0) > max(np.linalg.norm(h1-tipp),np.linalg.norm(h0-tipp)):
                        denom = lds[0] * (lds[5] - lds[3]) - lds[1] * (lds[4] - lds[2]) + lds[4] * lds[3] - lds[5] * lds[2]
                        if np.abs(denom)>.0000000001:
                            dLdx[i_node[0]] += np.sign(denom) * (lds[5] - lds[3]) / np.abs(denom)
                            dLdy[i_node[0]] += -np.sign(denom) * (lds[4] - lds[2]) / np.abs(denom)

                    #DEBUG

        #             if i_node[0] == test_nd_ind:
        #                 opplab = self.node_refs[i_node[1]].label + '-to-' + self.node_refs[i_node[2]].label
        #                 debug_file.write('Sibling\t' + opplab + '\t' + str(np.sign(denom) * (lds[5] - lds[3]) / np.abs(denom))
        #                                  + '\t' + str(-np.sign(denom) * (lds[4] - lds[2]) / np.abs(denom)) + '\t'
        #                                  + str(np.abs(denom) / np.linalg.norm(lds[2:4] - lds[4:6])) + '\n')
        #
        # debug_file.close()

        # if GLOBAL_DEBUG == True:
        #     print 'calculating dxdt and dydt'
        # dxdt = np.dot(np.diag(np.multiply(-1 * lens, np.sin(thetas))), M)  # [(2K-2) X (2K-2)] x [(2K-2) X (2K-2)]
        dxdt = (M.transpose()*np.multiply(-1 * lens, np.sin(thetas))).transpose()
        # if GLOBAL_DEBUG == True:
        #     print 'dxdt done...'
        # dydt = np.dot(np.diag(np.multiply(lens, np.cos(thetas))), M)  # [(2K-2) X (2K-2)] x [(2K-2) X (2K-2)]
        dydt = (M.transpose() * np.multiply(lens, np.cos(thetas))).transpose()
        # if GLOBAL_DEBUG == True:
        #     print 'dydt done...'
        # print 'Total Log-Norms: %s' % total_loss
        gradients = np.dot(dLdx, dxdt) + np.dot(dLdy, dydt)
        # if GLOBAL_DEBUG == True:
        #     print 'done making gradietns, the shape is: %s' % tuple(gradients.shape)
        # print gradients.shape
        toc = datetime.datetime.now()
        # print 'Total time to calc gradients: %s' % (toc-tic)
        return gradients

    def get_delaunay_leaf_segments(self, pts_leaves_bln,  tri):
        seg_inds_list = []  # list of pairs representing segments between leaves based on indices pulled from the simplices
        H = tri.simplices.shape[0]
        for i in range(H):
            # TODO: this version is for when we just consider distances between at least one leaf
            j1 = pts_leaves_bln[tri.simplices[i, 0]]
            j2 = pts_leaves_bln[tri.simplices[i, 1]]
            j3 = pts_leaves_bln[tri.simplices[i, 2]]
            if j1 == True or j2 == True:
                seg_inds_list.append(tri.simplices[i, 0:2])
            if j1 == True or j3 == True:
                seg_inds_list.append(np.vstack((tri.simplices[i, 0], tri.simplices[i, 2])).transpose())
            if j2 == True or j3 == True:
                seg_inds_list.append(tri.simplices[i, 1:3])

        # add each segment calc to the partials
        seg_inds = np.vstack(tuple(seg_inds_list))
        return seg_inds

    def get_delaunay_leaf_to_edge_segments(self, tri, pts_nparr):
        leaf_to_edge_segs=[]

        H = tri.simplices.shape[0]
        for i in range(H):
            inds = tri.simplices[i,:]
            j0j1 = np.linalg.norm(pts_nparr[inds[0], :] - pts_nparr[inds[1], :])
            j0j2 = np.linalg.norm(pts_nparr[inds[0], :] - pts_nparr[inds[2], :])
            j1j2 = np.linalg.norm(pts_nparr[inds[1], :] - pts_nparr[inds[2], :])
            if j0j1>j1j2:
                if j0j2>j0j1:
                    hyp=(0,2); tipp=1
                else:
                    hyp=(0,1); tipp=2
            else:
                if j0j2>j1j2:
                    hyp=(0,2); tipp=1
                else:
                    hyp=(1,2); tipp=0

            # check to see if the hypoteneuse is an edge:
            if self.node_refs[inds[tipp]].is_leaf():
                if self.node_refs[inds[hyp[0]]].parent_node is not None and self.node_refs[inds[hyp[1]]].parent_node is not None:
                    if self.node_refs[inds[hyp[0]]].parent_node.index==inds[hyp[1]] or self.node_refs[inds[hyp[1]]].parent_node.index==inds[hyp[0]]:
                        leaf_to_edge_segs.append((inds[tipp],inds[hyp[0]],inds[hyp[1]]))

        return leaf_to_edge_segs

    def get_delaunay_trianglization(self):
        pts = {}
        ndct = 0
        lct = 0
        leaf_order = []
        node_order = []
        pts_lst_np = []
        pts_leaves_bln = []
        self.node_refs=[]

        #DEBUG
        # node_ref_file = open('C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\phylostrator-testing\\node_indices.txt', 'w')
        for i in self.myt.preorder_node_iter():
            npiloc = np.array([i.location[0], i.location[1]], dtype=np.float64)
            pts_lst_np.append(npiloc)
            pts[i.label] = {'npiloc': npiloc,
                            'leaf': i.is_leaf(),
                            'label': i.label,
                            'index': ndct,
                            'leaf_index': None}
            # node_ref_file.write(i.label + '\t' + str(ndct) + '\n')  #DEBUG
            self.node_refs.append(i)
            pts_leaves_bln.append(i.is_leaf())
            i.index = ndct
            if i.is_leaf() == True:
                pts[i.label]['leaf_index'] = lct
                lct += 1
                leaf_order.append(i.label)
            ndct += 1
            node_order.append(i.label)

        # node_ref_file.close() #DEBUG
        ptstup = tuple(pts_lst_np)
        pts_nparr = np.vstack(ptstup)
        tri = spat.Delaunay(pts_nparr)

        #DEBUG
        # tri_indices_file = 'C:\\Users\\miken\\Dropbox\\Grad School\\Phylogenetics\\work\\phylostrator-testing\\tri_simplices_list.txt'
        # np.savetxt(tri_indices_file,tri.simplices,delimiter = '\t')
        return ndct, node_order, pts, pts_leaves_bln, tri, pts_nparr

    def relocate_subtree_by_wedge_properties(self,node,wedge_angle=None):
        '''

        :param node:
        :return:
        '''
        preo = node.preorder_iter()
        nd = preo.next()
        temp_nu={}
        temp_nu[nd.id]=nd.right_wedge_border
        for i in preo:
            i.wedge_angle = i.percent_of_parent_wedge*i.parent_node.wedge_angle
            i.right_wedge_border = temp_nu[i.parent_node.id]
            temp_nu[i.parent_node.id]+=i.wedge_angle
            temp_nu[i.id]=i.right_wedge_border
            i.edge_segment_angle = i.right_wedge_border + i.wedge_angle/2

            xu = i.parent_node.location
            delta = i.edge_length
            x1 = xu[0] + delta * math.cos(i.edge_segment_angle)
            x2 = xu[1] + delta * math.sin(i.edge_segment_angle)
            i.location=(x1,x2)
            i.deflect_angle = i.edge_segment_angle-i.parent_node.edge_segment_angle


    def get_de_facto_spread_angle(self,node):
        '''

        :param node:
        :return:
        '''
        start = node.parent_node.location
        angles = []
        for i in node.leaf_iter():
            xi = i.location
            ang = math.atan2(xi[1]-start[1],xi[0]-start[0])
            if ang < 0:
                ang = 2*math.pi - ang
            angles.append(ang)
        return min(angles), max(angles)

    # def angle_spread_extension(self):
    #     pass

    def get_max_dims(self):
        xma=float(0)
        xmi=float(0)
        yma=float(0)
        ymi=float(0)

        for i in self.node_labels.keys():
            x=self.node_labels[i]['x'][0]
            y=self.node_labels[i]['x'][1]
            if x>xma and x is not None:
                xma=x
            if x<xmi and x is not None:
                xmi=x
            if y>yma and y is not None:
                yma=y
            if y<ymi and y is not None:
                ymi=y
        self.max_dims=(xmi-.0001,xma+.0001,ymi-.0001,yma+.0001)
        return (xmi-.0001,xma+.0001,ymi-.0001,yma+.0001)

    def get_segments(self):
        '''
        sets the 'segments' property to be a list of tuples of tuples [((x11,y11),(x12,y12)),...]
        '''

        self.segments=[]
        view_segments={}

        for i in self.myt.preorder_node_iter():
            if i.parent_node is not None:
                i.edge.viewer_edge=None
                i.viewer_node=None
                # x1 = self.node_labels[i.parent_node.label]['x']
                # x2 = self.node_labels[i.label]['x']
                x1 = i.parent_node.location
                x2 = i.location
                old_label=self.node_labels[i.label]['old_label']
                try:
                    bootstrap=float(old_label)
                except:
                    bootstrap=None
                ed = ViewerEdge(x1,x2,None,None,i.edge.label,bootstrap,i.edge)
                i.edge.viewer_edge=ed
                # nd=ViewerNode(x2,node_ref=i,theta=self.node_labels[i.label]['t'])
                nd = ViewerNode(x2, node_ref=i, theta=i.right_wedge_border)
                i.viewer_node=nd
                self.segments.append((x1,x2))
                view_segments[i.edge.label]=ed
            else:
                i.edge.viewer_edge=None
                i.viewer_node=None
        return view_segments

    def prepare_tree(self):
        # print self.myt.internal_edges()[1].length
        rooted = False
        for i in self.myt.preorder_edge_iter():
            if i.length==None:
                i.length=0
                rooted=True
                # break
        if rooted==False:
            self.myt.reroot_at_edge(self.myt.internal_edges()[1])
        # self.myt.reroot_at_midpoint()
        # rooted = True

        lab=1
        for i in self.myt.preorder_edge_iter():
            i.label='edge'+str(lab)
            lab+=1

        lab=1
        alllabs=set([])
        ct = 0
        for i in self.myt.postorder_node_iter():
            oldlab=i.label
            i.id = ct
            ct+=1
            # i.label='label' + str(lab)
            # lab+=1
            # if i.is_leaf()==True:
            #     taxname=i.taxon.label
            # else:
            #     taxname=''
            # self.node_labels[i.label]={'x':None, 'l':None, 'w':None, 't':None, 'nu':None, 'theta':0, 'old_label':oldlab, 'taxon_label':taxname}
            if i.taxon == None:
                if i.label == None or i.label in alllabs:
                    # print i.__dict__
                    i.label='label' + str(lab)
                    lab+=1
                    if i.is_leaf()==True:
                        taxname=i.taxon.label
                    else:
                        taxname=''
                else:
                    taxname=i.label
            else:
                i.label=i.taxon.label
                taxname=i.label
            alllabs.add(oldlab)
            self.node_labels[i.label]={'x':None, 'l':None, 'w':None, 't':None, 'nu':None, 'theta':0, 'old_label':oldlab, 'taxon_label':taxname}


    # def get_selected(self,tx):
    #     #TODO: Make sure this is deprecated
    #     # print 'getting x coords for selected taxa'
    #     settx=set(tx)
    #     self.selected=[]
    #     # ct = 0
    #     for i in self.myt.leaf_node_iter():
    #         # ct +=1
    #         # if ct % 1000==0:
    #         #     print str(i.taxon.label) + ' - ' + type(i.taxon.label)
    #         if str(i.taxon.label) in settx:
    #             self.selected.append(self.node_labels[i.label]['x'])
    #     return self.selected

    def get_leaf_node_coords(self):
        '''
        Just makse a dictionary of all the leaf node descriptions along with their coordaintes and a refernce to the
            node object that stores them
        '''
        self.leaf_node_coords={}
        for i in self.myt.leaf_node_iter():
            # args={'x':self.node_labels[i.label]['x'],'node_ref':i}
            args = {'x': i.location, 'node_ref': i}
            args['drawn']=False
            args['color']=None
            args['node_annotation']=None
            self.leaf_node_coords[i.taxon.label]=args.copy()
            del args

    # def get_view_nodes(self):
    #     '''
    #     DEPRECATED
    #     :return: big list of veiwer nodes
    #     '''
    #     print 'get_vew_nodes() called, tree_manipulator.py, line 483'
    #     view_nodes={}
    #     for i in self.myt.preorder_node_iter():
    #         vn=ViewerNode(x=self.node_labels[i.label]['x'],node_ref=i,theta=self.node_labels[i.label]['theta'])
    #         view_nodes[i.label] = vn
    #     return view_nodes

    def refresh_all(self):
        self.get_radial_phylogram()
        self.get_segments()
        self.get_max_dims()

    def deform_clade_by_wedge_and_radians(self,myedge,width_radians, right_edge_radians):
        nd = myedge.head_node
        init_ww = self.node_labels[nd.label]['w']
        init_t = self.node_labels[nd.label]['t']


        pr = nd.preorder_iter()
        a=pr.next()
        self.node_labels[a.label]['w']=width_radians
        self.node_labels[a.label]['t']=right_edge_radians
        self.node_labels[a.label]['nu']=right_edge_radians
        ref_ct = float(len(a.leaf_nodes()))
        # a=nd
        # self.node_labels[a.label]['w']=width_radians
        # self.node_labels[a.label]['t']=right_edge_radians
        # self.node_labels[a.label]['nu']=right_edge_radians
        # ref_ct = float(len(a.leaf_nodes()))

        for i in pr:
            # k+=1
            # print k
            ww=float(len(i.leaf_nodes()))/ref_ct*width_radians
            self.node_labels[i.label]['w']=ww   # wedge angle
            self.node_labels[i.label]['t']=self.node_labels[i.parent_node.label]['nu'] # angle of right wedge border
            self.node_labels[i.label]['nu']=self.node_labels[i.label]['t']
            thetav=self.node_labels[i.parent_node.label]['nu']+ww/2
            self.node_labels[i.label]['theta']=thetav
            self.node_labels[i.parent_node.label]['nu']+=ww
            xu=self.node_labels[i.parent_node.label]['x']
            delta=i.edge_length
            x1=xu[0]+delta*math.cos(thetav)
            x2=xu[1]+delta*math.sin(thetav)
            # x1_orig = xu[0] + delta * math.cos(thetav)
            # x2_orig = xu[1] + delta * math.sin(thetav)
            # x1 = x1_orig*math.cos(self.rotation)-x2_orig*math.sin(self.rotation)
            # x2 = x1_orig*math.sin(self.rotation)+x2_orig*math.cos(self.rotation)
            self.node_labels[i.label]['x']=(x1,x2)

        self.get_segments()
        self.get_max_dims()

class AnnotationData():

    def __init__(self,filepath,filter_vals = None):
        self.path = filepath
        self.import_data(filter_vals)
        self.filter1_field=None
        self.filter1_options=set([])
        self.filter1_values=set([])
        self.filter2_field = None
        self.filter2_options = set([])
        self.filter2_values = set([])

        self.selected_annotation_field=None
        self.active_unique_annotation_values=set([])

    def import_data(self,filter_vals = None):
        f=open(self.path,'r')
        self.headers = f.readline().strip().split('\t')
        self.data = {}
        if filter_vals is None:
            for i in f:
                a=i.strip().split('\t')
                self.data[a[0]]=tuple(a)
        else:
            for i in f:
                a=i.strip().split('\t')
                if a[0] in filter_vals:
                    self.data[a[0]]=tuple(a)
        f.close()

    def load_filter1(self,header):
        f1_vals=[]

        self.filter1_field=header
        if self.filter1_field=='(none)':
            self.filter1_options = set([])
            self.filter1_values = set([])
        else:
            f1_col = self.headers.index(header)
            for i in self.data.values():
                f1_vals.append(i[f1_col])

        self.filter1_options=set(f1_vals)
        return self.filter1_options

    def load_filter2(self, header):
        f2_vals = []
        print "getting values for header %s" % header
        self.filter2_field = header
        if self.filter2_field == '(none)':
            self.filter2_options = set([])
            self.filter2_values = set([])
        else:
            f2_col = self.headers.index(header)
            f1_col = self.headers.index(self.filter1_field)
            for i in self.data.values():
                if len(self.filter1_values) == 0 or i[f1_col] in self.filter1_values:
                    f2_vals.append(i[f2_col])

        self.filter2_options = set(f2_vals)
        return self.filter2_options

    def process_filter2(self, selections):
        if len(selections) == 0:
            self.filter2_values = set([])
        else:
            self.filter2_values = set(selections)

    def process_filter1(self, selections):
        if len(selections) == 0:
            self.filter1_values = set([])
        else:
            self.filter1_values = set(selections)

    def get_active_unique_annotation_values(self):
        # print self.selected_annotation_field
        if self.selected_annotation_field is None or self.selected_annotation_field == '':
            return None
        if self.active_unique_annotation_values is not None:
            del self.active_unique_annotation_values
        uav = []
        ann_col = self.headers.index(self.selected_annotation_field)
        # print ann_col
        if self.filter1_field is not None:
            f1_col = self.headers.index(self.filter1_field)
        if self.filter2_field is not None:
            f2_col = self.headers.index(self.filter2_field)

        self.grouped={}
        setuav=set([])
        for i in self.data.keys():
            keep = True
            if self.filter1_field is not None and len(self.filter1_values) > 0 and self.data[i][f1_col] not in self.filter1_values:
                keep = False
            elif self.filter2_field is not None and len(self.filter2_values) > 0 and self.data[i][f2_col] not in self.filter2_values:
                keep = False
            if keep == True:
                # uav.append(self.data[i][ann_col])
                ann_col_val = self.data[i][ann_col]
                if ann_col_val in setuav:
                    self.grouped[ann_col_val].append(i)
                else:
                    # print self.data[i]
                    # print "%s - %s" % (ann_col_val,str(setuav))
                    setuav.update(set([self.data[i][ann_col]]))
                    self.grouped[ann_col_val]=[i]

        self.active_unique_annotation_values = setuav
        # print setuav
        return setuav

    def get_EFDIDs_grouped_by(self,header_field):
        self.get_active_unique_annotation_values()
        return self.grouped

class SfldAnnotationData():
    '''
    must be tab-separated values
    must have one of the header fields called "efd_id"
    '''

    def __init__(self, filepath,key_field='Observation ID'):
        self.f=open(filepath,'r')
        self.data={}
        self.uniques={}
        # key_field='seqname'
        key_field='seqnum'

        #get field names
        self.fieldnames=self.f.readline().strip().split('\t')
        try:
            # self.efdid_index=self.fieldnames.index('efd_id')
            self.efdid_index=self.fieldnames.index(key_field)
            self.annotation_fields=self.fieldnames[:self.efdid_index] + self.fieldnames[(self.efdid_index+1):]
            self.import_data()
        except:
            print 'No column called %s in the node_annotation file %s' % (key_field,filepath)
            self.efdid_index=None
            self.annotation_fields=None

    def import_data(self):
        '''
        method run at inititalization to import all the data
        :return:
        '''
        uniques_lists={}
        for i in range(len(self.fieldnames)):
            if i != self.efdid_index:
                uniques_lists[self.fieldnames[i]]=[]

        for i in self.f:
            a=i.strip().split('\t')
            args={}
            id = a[self.efdid_index]
            for i in range(len(self.fieldnames)):
                if i != self.efdid_index:
                    args[self.fieldnames[i]]=a[i]
                    uniques_lists[self.fieldnames[i]].append(a[i])
            self.data[id]=args.copy()
            del args

        for i in uniques_lists.keys():
            self.uniques[i]=list(set(uniques_lists[i]))

        del uniques_lists

    def get_EFDIDs_grouped_by(self,header_field):
        # try:
        assert header_field in self.fieldnames
        # except:
        #     print "get_EFIDs_grouped_by called with missing header field"
        #     return {}

        grouped={}
        for i in self.data:
            a=self.data[i][header_field]
            if a in grouped.keys():
                grouped[a].append(i)
            else:
                grouped[a]=[i]

        for i in grouped:
            grouped[i]=set(grouped[i])

        # print grouped
        return grouped
