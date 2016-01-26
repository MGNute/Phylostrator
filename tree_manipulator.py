__author__ = 'Michael'

import math
import dendropy
from my_globals import *

class Radial_Phylogram():
    max_dims=None

    def __init__(self,tp=None):
        self.treepath=''
        self.myt=None
        self.node_labels={}
        self.segments=[]
        if tp is not None:
            self.set_treepath(tp)


    def set_treepath(self,tp):
        self.treepath=tp
        self.myt=dendropy.Tree.get(file=open(self.treepath,'r'),schema="newick")
        self.get_radial_phylogram()

    def get_radial_phylogram(self):
        # myt=set_treepath(tp)
        self.prepare_tree()
        for i in self.myt.postorder_node_iter():
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
        self.node_labels[r.label]['w']=2*math.pi
        self.node_labels[r.label]['t']=0.0
        self.node_labels[r.label]['nu']=0.0
        leafct=len(r.leaf_nodes())

        # k=0
        for i in pr:
            # k+=1
            # print k
            ww=float(len(i.leaf_nodes()))/leafct*2*math.pi
            self.node_labels[i.label]['w']=ww
            self.node_labels[i.label]['t']=self.node_labels[i.parent_node.label]['nu']
            self.node_labels[i.label]['nu']=self.node_labels[i.label]['t']
            thetav=self.node_labels[i.parent_node.label]['nu']+ww/2
            self.node_labels[i.parent_node.label]['nu']+=ww
            xu=self.node_labels[i.parent_node.label]['x']
            delta=i.edge_length
            x1=xu[0]+delta*math.cos(thetav)
            x2=xu[1]+delta*math.sin(thetav)
            self.node_labels[i.label]['x']=(x1,x2)

    def get_max_dims(self):
        xma=float(0)
        xmi=float(0)
        yma=float(0)
        ymi=float(0)

        for i in self.node_labels.keys():
            x=self.node_labels[i]['x'][0]
            y=self.node_labels[i]['x'][1]
            if x>xma:
                xma=x
            if x<xmi:
                xmi=x
            if y>yma:
                yma=y
            if y<ymi:
                ymi=y
        self.max_dims=(xmi-.0001,xma+.0001,ymi-.0001,yma+.0001)
        return (xmi-.0001,xma+.0001,ymi-.0001,yma+.0001)

    def get_segments(self):
        '''
        sets the 'segments' property to be a list of tuples of tuples.
        '''

        self.segments=[]

        for i in self.myt.preorder_node_iter():
            if i.parent_node is not None:
                x1=self.node_labels[i.parent_node.label]['x']
                x2=self.node_labels[i.label]['x']
                self.segments.append((x1,x2))
            # print self.node_labels[i.label]

    def prepare_tree(self):
        self.myt.reroot_at_edge(self.myt.internal_edges()[1])

        lab=1
        for i in self.myt.postorder_node_iter():
            i.label=str(lab)
            self.node_labels[str(lab)]={'x':None, 'l':None, 'w':None, 't':None, 'nu':None}
            lab+=1

