__author__ = 'Michael'

import math
import dendropy
# from my_globals import *


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
    max_dims=None

    def __init__(self,tp=None):
        self.treepath=''
        self.myt=None
        self.node_labels={}
        self.segments=[]
        self.selected=[]
        self.leaf_node_coords={}
        self.selected_color=None
        if tp is not None:
            self.set_treepath(tp)

    def set_treepath(self,tp):
        self.treepath=tp
        self.myt=dendropy.Tree.get(file=open(self.treepath,'r'),schema="newick",preserve_underscores=True)
        self.get_radial_phylogram()
        self.get_max_dims()
        self.get_leaf_node_coords()

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

        for i in self.myt.preorder_node_iter():
            if i.parent_node is not None:
                x1=self.node_labels[i.parent_node.label]['x']
                x2=self.node_labels[i.label]['x']
                self.segments.append((x1,x2))
            # print self.node_labels[i.label]

    def prepare_tree(self):
        # print self.myt.internal_edges()[1].length
        rooted = False
        for i in self.myt.preorder_edge_iter():
            if i.length==None:
                rooted=True
                break
        if rooted==False:
            self.myt.reroot_at_edge(self.myt.internal_edges()[1])

        lab=1
        for i in self.myt.postorder_node_iter():
            i.label=str(lab)
            self.node_labels[str(lab)]={'x':None, 'l':None, 'w':None, 't':None, 'nu':None}
            lab+=1

    def get_selected(self,tx):
        #TODO: Make sure this is deprecated
        # print 'getting x coords for selected taxa'
        settx=set(tx)
        self.selected=[]
        # ct = 0
        for i in self.myt.leaf_node_iter():
            # ct +=1
            # if ct % 1000==0:
            #     print str(i.taxon.label) + ' - ' + type(i.taxon.label)
            if str(i.taxon.label) in settx:
                self.selected.append(self.node_labels[i.label]['x'])
        return self.selected

    def get_leaf_node_coords(self):
        '''
        Just makse a dictionary of all the leaf node descriptions along with their coordaintes and a refernce to the
            node object that stores them
        '''
        for i in self.myt.leaf_node_iter():
            args={'x':self.node_labels[i.label]['x'],'node_ref':i}
            args['drawn']=False
            args['color']=None
            args['node_annotation']=None
            self.leaf_node_coords[i.taxon.label]=args.copy()
            del args


class SfldAnnotationData():
    '''
    must be tab-separated values
    must have one of the header fields called "efd_id"
    '''

    def __init__(self, filepath):
        self.f=open(filepath,'r')
        self.data={}
        self.uniques={}

        #get field names
        self.fieldnames=self.f.readline().strip().split('\t')
        try:
            self.efdid_index=self.fieldnames.index('efd_id')
            self.annotation_fields=self.fieldnames[:self.efdid_index] + self.fieldnames[(self.efdid_index+1):]
            self.import_data()
        except:
            print 'No column called \"efd_id\" in the node_annotation file %s' % filepath
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



