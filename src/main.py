# -*- coding: utf-8 -*-
'''
Created on 16/07/2013

@author: roque
'''
import sys
from reader import Reader
from machine_learning.feature_extractor import FeatureExtractor
from machine_learning.baselines import BaseLines
from evaluator import Evaluator
from cst.relations_cst import CSTRelations

if __name__ == '__main__':
    option = sys.argv[1]

    folder_corpus = "../resource/data/cstnews_corpus/"
    folder_manual_alignments = "../resource/data/manual_alignments/"
    folder_cst_relations = "../resource/data/cst_relations/"
    file_matrix_features = "../resource/data/matriz.txt"
    
    reader = Reader()
    evaluator = Evaluator()
    manual_alignments = reader.read_alignments(folder_manual_alignments)
    cluster_list = reader.read_clusters(folder_corpus)
    
    
    if option == "superficial":
        ##################### Baseline Methods ################## 
        bs = BaseLines(cluster_list)
        bs.evaluate_separated(0.295, mode=1)# modes: 1=word overlap, 2=relative position, 3=relative size
        #bs.evaluate_together([0.4, 0.3, 0.6])#word overlap, relative position and relative size
        baseline_alignments = bs.get_baseline_alignments()
        evaluator.evaluate_accumulative(manual_alignments, baseline_alignments)
        evaluator.print_measures()
        #####################ooooooooooooooo#####################  
        
     
    elif option == "deep":
        ##################### CST's Method #####################
        cst = CSTRelations()
        cst_alignments  = cst.read_relations_cst(folder_cst_relations, 'direct')
        evaluator.evaluate_accumulative(manual_alignments, cst_alignments)
        evaluator.print_measures()
        ####################ooooooooooooooo#####################
     
    
    elif option == "hybrid":
        ############### Machine Learning's Method ###############  
        fe = FeatureExtractor(cluster_list, folder_cst_relations, manual_alignments)
        fe.evaluate()
        fe.print_data(file_matrix_features)
        #####################ooooooooooooooo#####################
        
    
    elif option == "jing":
        ##################### Jing's Method #####################
        jing_alignments = dict()    
        for id_cluster, cluster in cluster_list.items():
            print("Cluster", id_cluster)
            cluster.create_pairs()
            cluster.create_hmms()
            jing_alignments[id_cluster] = cluster.get_alignment()
                  
        evaluator.evaluate_accumulative(manual_alignments, jing_alignments)
        evaluator.print_measures()
        #####################ooooooooooooooo##################### 
    
