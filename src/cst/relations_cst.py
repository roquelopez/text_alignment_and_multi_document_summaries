# -*- coding: utf-8 -*-
'''
Created on 01/08/2013

@author: roque
'''
import os
import utils
from bs4 import BeautifulSoup

class CSTRelations(object):
    '''
    Reads the cst relations
    '''

    def read_relations_cst(self, folder_path, mode='direct'):
        ''' Selects the mode to read the cst relations '''
        if mode == 'direct':
            return self.__direct_relations(folder_path)
        elif mode == 'indirect':
            return self.__indirect_relations(folder_path)
        else:
            print("Invalid mode")

    def __direct_relations(self, folder_path):
        ''' Creates the cst direct relations '''
        cluster_list = dict()# it contents the cst alignments: {'id_cluster':{'id_sentence':[doc1,...,docn]}}
        
        for id_cluster in os.listdir(folder_path):
            text_document = utils.read_file(os.path.join(folder_path, id_cluster, 'Relacoes_Sumario.cst'))
            cluster_list[id_cluster] = dict()
            soup = BeautifulSoup(text_document)
         
            for relation in soup.findAll('r'):
                if relation.get('sdid').find('_sumario_') > -1:
                    id_sentence_summary = relation.get('ssent')
                    if not id_sentence_summary in cluster_list[id_cluster]: cluster_list[id_cluster][id_sentence_summary] = list()
                    if not (relation.get('tdid'), relation.get('tsent')) in cluster_list[id_cluster][id_sentence_summary]:
                        cluster_list[id_cluster][id_sentence_summary].append((relation.get('tdid'), relation.get('tsent')))
                
                elif relation.get('tdid').find('_sumario_') > -1:
                    id_sentence_summary = relation.get('tsent')
                    if not id_sentence_summary in cluster_list[id_cluster]: cluster_list[id_cluster][id_sentence_summary] = list()
                    if not (relation.get('sdid'), relation.get('ssent')) in cluster_list[id_cluster][id_sentence_summary]:
                        cluster_list[id_cluster][id_sentence_summary].append((relation.get('sdid'), relation.get('ssent')))
        
        return cluster_list
    
    def __indirect_relations(self, folder_path):
        ''' Creates the cst indirect relations '''
        cluster_list = dict()# it contents the cst alignments: {'id_cluster':{'id_sentence':[doc1,...,docn]}}
        direct_relations = self.__direct_relations(folder_path)
        
        for id_cluster in os.listdir(folder_path):
            text_document = utils.read_file(os.path.join(folder_path, id_cluster, 'Relacoes_Sumario.cst'))
            cluster_list[id_cluster] = dict()
            soup = BeautifulSoup(text_document)
         
            for relation in soup.findAll('r'): 
                if relation.get('sdid').find('_sumario_') == -1:       
                    id_sentence_summary = self.__search_sentence_summary(relation.get('sdid'), relation.get('ssent'), direct_relations[id_cluster])
                    if id_sentence_summary is not None and relation.get('tdid').find('_sumario_') == -1: 
                        if not id_sentence_summary in cluster_list[id_cluster]: cluster_list[id_cluster][id_sentence_summary] = list()
                        if not (relation.get('tdid'), relation.get('tsent')) in cluster_list[id_cluster][id_sentence_summary]:
                            cluster_list[id_cluster][id_sentence_summary].append((relation.get('tdid'), relation.get('tsent')))
            
        return cluster_list
    
    def read_complete_relations(self, folder_path):
        ''' Creates the cst direct relations '''
        cluster_list = dict()# it contents the cst alignments: {'id_cluster':{'id_sentence':[doc1,...,docn]}}

        for id_cluster in os.listdir(folder_path):
            text_document = utils.read_file(os.path.join(folder_path, id_cluster, 'Relacoes_Sumario.cst'))
            cluster_list[id_cluster] = dict()
            soup = BeautifulSoup(text_document)
         
            for relation in soup.findAll('r'):
                if relation.get('sdid').find('_sumario_') > -1:
                    id_sentence_summary = relation.get('ssent')
                    if not id_sentence_summary in cluster_list[id_cluster]: cluster_list[id_cluster][id_sentence_summary] = list()
                    if not (relation.get('tdid'), relation.get('tsent'), relation.find('relation').get('type')) in cluster_list[id_cluster][id_sentence_summary]:
                        cluster_list[id_cluster][id_sentence_summary].append((relation.get('tdid'), relation.get('tsent'), relation.find('relation').get('type')))
                
                elif relation.get('tdid').find('_sumario_') > -1:
                    id_sentence_summary = relation.get('tsent')
                    if not id_sentence_summary in cluster_list[id_cluster]: cluster_list[id_cluster][id_sentence_summary] = list()
                    if not (relation.get('sdid'), relation.get('ssent'), relation.find('relation').get('type')) in cluster_list[id_cluster][id_sentence_summary]:
                        cluster_list[id_cluster][id_sentence_summary].append((relation.get('sdid'), relation.get('ssent'), relation.find('relation').get('type')))
        
        return cluster_list
    
    def __search_sentence_summary(self, id_document, id_sentence, direct_relations):
        ''' Returns the id of the sentence in the summary '''
        for id_sentence_summary, relations in direct_relations.items():
            if (id_document, id_sentence) in relations:
                return id_sentence_summary
        return None
    