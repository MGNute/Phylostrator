__author__ = 'Michael'

import platform
# TODO: get ride of this module eventually

if platform.system()=='Darwin':
    test_tp='/Users/michaelnute/GradSchool/Research/Phylogenetics/results/2016-01-protein-sfld/sf1_fasttree.tre'
elif platform.system()=='Windows':
    # test_tp='C:/Users/Michael/Grad School Stuff/Research/Phylogenetics/results/2016-01-protein-sfld/sf1/sf1.tre'
    test_tp='C:/Users/Michael/Grad School Stuff/Research/Phylogenetics/results/2016-02-protein-alignment/scop/t99-t108_upp_alignment_masked.fasttree'
    # test_tp='C:/Users/Michael/Grad School Stuff/Research/Phylogenetics/results/2015_04_20_baliphy_in_UPP/data_from_nam/pasta/gutell/16S.T/1/pasta/pastajob-nobs-small.tre'
    # test_folder='C:/Users/Michael/Grad School Stuff/Research/Phylogenetics/results/2016-01-protein-sfld/sf1'
    test_folder='C:/Users/Michael/Grad School Stuff/Research/Phylogenetics/results/2016-02-protein-alignment/scop/'
    test_image='C:/Users/Michael/Grad School Stuff/Research/Phylogenetics/results/2016-01-protein-sfld/sf1/Picture2.jpg'

    test_annotation=test_folder + '/sfld_superfamily_1_excel.tsv'

