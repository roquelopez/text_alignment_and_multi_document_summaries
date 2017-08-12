# -*- coding: utf-8 -*-
'''
Created on 17/07/2013

@author: roque
'''
import os
import re
import utils
from jing.cluster import Cluster
from bs4 import BeautifulSoup


class Reader(object):
    '''
    Reads a summary and the original documents in file format
    '''

    def read_alignments(self, folder_path, weka_format=False):
        ''' Reads the xml files with the manual alignments '''
        cluster_list = dict()# it contents the manual alignments: {'id_cluster':{'id_sentence':[doc1,...,docn]}}
        for file in os.listdir(folder_path):
            text_document = utils.read_file(os.path.join(folder_path, file))
            id_cluster = file.split('_')[0]
            cluster_list[id_cluster] = dict()
            soup = BeautifulSoup(text_document)
         
            for sentence in soup.findAll('align'):
                cluster_list[id_cluster][sentence.get('sent')] = list()
                for doc in sentence.findAll('doc'):
                    if weka_format:
                        new_name = doc.get('name').split('_')[0] # format for Weka's alignments
                        cluster_list[id_cluster][sentence.get('sent')].append((new_name, doc.get('sent')))# format for Weka's alignments
                    else:
                        cluster_list[id_cluster][sentence.get('sent')].append((doc.get('name'), doc.get('sent'), doc.get('type').strip()))
        return cluster_list
    
    def read_clusters(self, folder_path):
        ''' Reads the test files '''
        files = os.listdir(folder_path) 
        #files.sort()
        summaries = [x for x in files if x.find('_sumario_') > 0]
        cluster_list = dict()# cluster list
        
        for summary in summaries:
            id_cluster = summary.split('_')[0]
            raw_cluster = [x for x in files if x.find('_'+id_cluster+'_') > 0] 

            cluster = Cluster(True)
            text = utils.read_file(os.path.join(folder_path, summary))
            cluster.add_summary(text)
            
            for document_name in raw_cluster:
                text = utils.read_file(os.path.join(folder_path, document_name))
                cluster.add_document(document_name, text)
                 
            cluster_list[id_cluster] = cluster
        return cluster_list
    
    def read_weka_alignments(self, file_path):
        ''' Reads the txt file with the Weka's automatic alignments '''
        baseline_file = open(file_path, 'r')
        cluster_list = dict()# it contents the automatic alignments: {'id_cluster':{'id_sentence':[doc1,...,docn]}}
         
        while True:
            line = baseline_file.readline()
            if not line: break
            tmp = re.match('Cluster(\d+)_SumS(\d+)_DocC(\d+)_(.+).txt.segS(\d+):(.+)', line)
            #print(tmp.group(1), tmp.group(2), tmp.group(4), tmp.group(5))
            id_cluster = 'C' + tmp.group(1)
            id_sent_summary = tmp.group(2)

            if id_cluster not in cluster_list: cluster_list[id_cluster] = dict()
            if id_sent_summary not in cluster_list[id_cluster]: cluster_list[id_cluster][id_sent_summary] = list()
            cluster_list[id_cluster][id_sent_summary].append((tmp.group(4), tmp.group(5)))

        baseline_file.close()

        return cluster_list
