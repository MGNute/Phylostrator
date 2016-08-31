__author__ = 'Michael'
import copy
import dendropy
import numpy as np
from my_globals import *
nt_alphabet=['A','C','G','T','U','M','N']


def remove_all_blank_columns(fasta_dict,same_length_check=True):
    """
    Takes a dictionary representing a fasta file and removes any columns that are blank for all taxa. Data are
    assumed to be aligned starting with the first column in each string.

    NOTE: the operations in this function are in-place on the object provided by pythons nature, so while it
    returns a dictionary, catching the return value is not strictly necessary and the input will be
    modified after the fact.

    :param fasta_dict (dict): fasta dictionary (keys=taxon names, values=alignment strings)
    :param same_length_check (boolean) : OPTIONAL (default=True) If True, will throw an error if all sequences
        in fasta_dict are not the same length.
    :return: fasta_dict: dictionary with columns removed.
    """
    num_seqs=len(fasta_dict.values())
    seq_len = len(fasta_dict.values()[0])
    # print "#columns: %s" % seq_len
    new_dict={}
    for i in fasta_dict.keys():
        new_dict[i]=''

    # check that all the sequences are the same length
    if same_length_check==True:
        for i in fasta_dict.values():
            if len(i) <> seq_len:
                # print 'The sequences were not all the same length.'
                return -1

    # identify columns that are blank for every taxon
    all_blanks_list = []
    # print "# blanks: %s" % len(all_blanks_list)
    for i in range(seq_len):
        allblank=True
        for j in fasta_dict.values():
            if j[i]<>'-':
                allblank=False
                break
        if allblank==True:
            all_blanks_list.append(i)

    non_blanks=list(set(range(seq_len)).difference(set(all_blanks_list)))
    non_blanks.sort()
    # print "# non-blanks: %s" % len(non_blanks)


    # remove those columns (in place, so do it in reverse order)
    # if len(all_blanks_list)>0:
    #     all_blanks_list.sort(reverse=True)
    #     print len(all_blanks_list)
    #
    #     for i in all_blanks_list:
    #         for k in fasta_dict.keys():
    #             j=fasta_dict[k]
    #             fasta_dict[k]=j[0:i-1] + j[i:]
    # #         for j in fasta_dict.values():
    #       #     j = j[0:i-1] + j[i:]
    for i in non_blanks:
        for j in fasta_dict.keys():
            new_dict[j]=new_dict[j]+fasta_dict[j][i]

    lents=[]
    for i in new_dict.values():
        lents.append(len(i))
    print lents
    return new_dict

def nucleotide_to_int(nt):
    # 0 is the blank character
    if nt not in nt_alphabet:
        return 99
    return nt_alphabet.index(nt)+1

def int_to_nucleotide(nt):
    # 0 is the blank character
    if nt>5:
        return '?'
    return nt_alphabet[nt-1]


def read_from_fasta(file_path):
    """
    Reads from a fasta file and returns a dictionary where keys are taxon names and values are strings
    representing the sequence.
    :param file_path (string): The full system-readable path to the fasta file
    :return: fasta (dict)
    """
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

def check_is_leaf(a):
    return a.is_leaf()

class MultipleSequenceAlignment():

    def __init__(self,refpath=None,estpath=None, treepath=None):
        self.refpath=refpath
        self.estpath=estpath
        self.treepath=treepath
        self.ref=None
        self.est=None
        self.node_order=[]
        if self.treepath==None:
            self.treepath=test_tre
        self.get_node_order()
        if self.refpath==None:
            self.refpath=test_aln_ref
        self.set_refpath()
        self.finalize_ref_alignment()
        if self.estpath==None:
            self.estpath=test_aln_est
        self.set_estpath()
        tp,fn= self.count_tp_fn()
        print "Reference Alignment Length:\t%s" % self.reflen
        print "Reference Homologs:\t%s" % tp
        print "Estimated Homologs:\t%s" % self.est_homologs
        print "Shared Homologs:\t%s" % self.shared_homologs

        self.write_column_wise_errors()


    def get_node_order(self):
        print "Reading reference tree and getting node order..."
        self.tree=dendropy.Tree.get(path=self.treepath,schema="newick")
        if len(self.node_order)>0:
            self.old_node_order=copy.deepcopy(self.node_order)
        self.node_order=[]
        self.node_order_lookup={}
        self.get_cladogram_segments()
        # ct=0

        # for i in self.tree.postorder_node_iter(filter_fn=check_is_leaf):
        #     self.node_order.append(i.taxon.label)
        #     self.node_order_lookup[i.taxon.label]=ct
        #     ct+=1


    def set_refpath(self):
        print "Reading reference alignment..."
        self.ref_temp=read_from_fasta(self.refpath)
        self.ref=remove_all_blank_columns(self.ref_temp)
        self.reflen=len(self.ref[self.ref.keys()[0]])
        self.msa_cols=[]
        for i in range(self.reflen):
            x=MSAColumn(i,self)
            self.msa_cols.append(x)

        # lookup position in alignment based on position in sequence
        self.ref_seq_colindices={}

        txct=0
        print "Updating reference alignment columns..."
        for i in self.ref.keys():
            if txct % 10 ==0:
                print "\trow: %s" % txct
            txct+=1

            seq=self.ref[i]
            slen=len(seq.replace('-',''))
            self.ref_seq_colindices[i]=np.zeros(slen,dtype=np.uint32)
            position=0
            for j in range(self.reflen):
                if seq[j]!='-':
                    self.ref_seq_colindices[i][position]=j
                    self.msa_cols[j].add_char(i,seq[j],position)
                    position+=1

    def finalize_ref_alignment(self):
        print "Finalizing reference alignment..."
        for i in range(self.reflen):
            if i % 250==0:
                print i
            self.msa_cols[i].populate_tp_matrix()

    def set_estpath(self):
        print "Reading Estimated Alignment..."
        self.est = read_from_fasta(self.estpath)
        self.est_seq_colindices={}
        for i in self.est.keys():
            position=0
            self.est_seq_colindices[i]=[]
            myseq=self.est[i]
            for j in range(len(self.est.values()[0])):
                if myseq[j]!='-':
                    self.est_seq_colindices[i].append(j)
                    position+=1

        self.est_homologs=0
        self.shared_homologs=0
        self.numtaxa=len(self.est.keys())
        print "Calculating homologs and updating reference alignment..."
        for i in range(self.numtaxa):
            if i % 10 ==0:
                print "\trow: %s" % i
            i_colinds=self.est_seq_colindices[self.est.keys()[i]]
            i_label=self.est.keys()[i]
            for j in range(i+1,self.numtaxa):
                j_colinds=self.est_seq_colindices[self.est.keys()[j]]
                j_label=self.est.keys()[j]
                common=set(i_colinds).intersection(set(j_colinds))
                for hom in common:
                    i_pos=i_colinds.index(hom)
                    j_pos=j_colinds.index(hom)
                    ref_pos_i=self.ref_seq_colindices[i_label][i_pos]
                    ref_pos_j=self.ref_seq_colindices[j_label][j_pos]
                    if ref_pos_i==ref_pos_j:
                        self.msa_cols[ref_pos_i].update_false_negative(i_label,j_label)
                        self.shared_homologs+=1
                    self.est_homologs+=1
                    # self.est_homologs.append((i_label,i_pos,j_label,j_pos))
    def write_column_wise_errors(self):
        outf=open(tree_ref_aln_fnfp_totxt,'w')
        for i in range(self.reflen):
            tp, fn=self.msa_cols[i].tp_fn_count()
            outf.write('%s,%s,%s\n' % (i,tp,fn))
        outf.close()

    def get_cladogram_segments(self, bottom=1260, top=1560, firstnode=53, spacing=6, horizontal=True, leafs_on_left_or_bottom=True):
        # for grid graphic:  bottom=700, top=1000, firstnode=53, spacing=6
        t=copy.deepcopy(self.tree)
        self.tree_vertices={}
        for i in t.postorder_edge_iter():
            if i.length is not None:
                i.length=1.0
        print "rerooting at midpoint..."
        t.reroot_at_midpoint()
        height=t.max_distance_from_root()
        incr = int(abs(top-bottom)/height)
        # incr = int((top-bottom)/height)

        ct = 0
        # ct_all=0
        self.node_added_order=[]
        for i in t.postorder_node_iter():
            # self.node_added_order.append(i)
            args={}
            if check_is_leaf(i)==True:
                self.node_order.append(i.taxon.label)
                self.node_order_lookup[i.taxon.label]=ct
                order=ct
                ct+=1
                # order = self.node_order_lookup[i.taxon.label]
                self.tree_vertices[i]=(bottom,firstnode+spacing*order)
                args={'nd':i,'vert':(bottom,firstnode+spacing*order),'cvs':None}
                self.node_added_order.append(args)
            else:
                maxht=0
                sum_horz=0.0
                ct_child=0
                cvs=[]
                for j in i.child_nodes():
                    cvs.append(self.tree_vertices[j])
                    # if len(self.node_added_order)<20:
                    #     print "ch: %s, %s" % self.tree_vertices[j]
                for k in cvs:
                    if k[0]> maxht:
                        maxht=k[0]
                    sum_horz+=k[1]
                    ct_child+=1
                newht=maxht + incr
                newcent=int(float(sum_horz)/ct_child)
                self.tree_vertices[i]=(newht,newcent)
                args={'nd':i,'vert':(newht,newcent),'cvs':copy.deepcopy(cvs)}
                self.node_added_order.append(args)

        self.segment_endpoints=[]
        for i in t.postorder_edge_iter():
            if i.length is not None:
                v1=self.tree_vertices[i.head_node]
                v2=self.tree_vertices[i.head_node.parent_node]
                self.segment_endpoints.append((v1[0],v1[1],v2[0],v1[1]))
                self.segment_endpoints.append((v2[0],v1[1],v2[0],v2[1]))

        self.t_copy=t

    # def update_false_negatives(self):
    #     for hom in self.est_homologs:
    #         if self.ref_seq_colindices[hom[0]][hom[1]]==self.ref_seq_colindices[hom[2]][hom[3]]:
    #             self.msa_cols[self.ref_seq_colindices[hom[0]][hom[1]]].update_false_negative(hom[0],hom[2])

    def count_tp_fn(self):
        tp=0
        fn=0
        for i in self.msa_cols:
            a,b=i.tp_fn_count()
            tp += a
            fn += b
        return (tp,fn)


class MSAColumn():
    def __init__(self,index,parent):
        self.index=index
        self.node_order_lookup=parent.node_order_lookup
        self.fn_mat=np.zeros((len(self.node_order_lookup),len(self.node_order_lookup)),dtype=np.uint8)
        self.tp_mat=np.zeros((len(self.node_order_lookup),len(self.node_order_lookup)),dtype=np.uint8)
        self.chars={}

    def tp_fn_count(self):
        a=len(self.chars)
        return ((a*(a-1) >> 1),np.sum(self.fn_mat)/2)

    def add_char(self,label,site_char,seq_position):
        self.chars[self.node_order_lookup[label]]=(nucleotide_to_int(site_char),seq_position)

    def populate_tp_matrix(self):
        numtaxa=len(self.chars.keys())
        for i in range(numtaxa):
            # ind_i=self.node_order_lookup[self.chars.keys()[i]]
            ind_i=self.chars.keys()[i]
            for j in range(i+1,numtaxa):
                ind_j=self.chars.keys()[j]
                self.tp_mat[ind_i,ind_j]=1
                self.tp_mat[ind_j,ind_i]=1
                self.fn_mat[ind_i,ind_j]=1
                self.fn_mat[ind_j,ind_i]=1

    def update_false_negative(self,i_label,j_label):
        i_row=self.node_order_lookup[i_label]
        j_row=self.node_order_lookup[j_label]
        self.fn_mat[i_row,j_row]=0
        self.fn_mat[j_row,i_row]=0