# -*- coding: utf-8 -*-

'''
Created on 25/09/2013

@author: roque
'''
import utils
from math import floor, ceil, fabs

class BaseLines(object):
    '''
    Superficial methods: Word Overlap, Relative Position and Relative Size 
    '''

    def __init__(self, cluster_list):
        self.__cluster_list = cluster_list
        self.__equals_words_atr = dict()
        self.__relative_position_atr = dict()
        self.__relative_size_atr = dict()
        self.__alignments = dict()#it contents the cst alignments: {'id_cluster':{'id_sentence':[doc1,...,docn]}}
    
    def evaluate_separated(self, threshold, mode=1):
        ''' Evaluate the alignment's set '''
        for id_cluster, cluster in self.__cluster_list.items():
            print("id_cluster", id_cluster)
            cluster.create_pairs()
            pair_list = cluster.get_pairs()
            self.__alignments[id_cluster] = dict()
            for id_pair, pair in pair_list.items():
                self.__evaluate_pairs_separated(id_cluster, id_pair, pair, threshold, mode)
    
    def __evaluate_pairs_separated(self, id_cluster, id_pair, pair, threshold, mode):
        ''' Evaluate the alignment between  a document and the summary '''
        summary_sentences = pair.get_raw_summary_sentences()
        document_sentences = pair.get_document_sentences()
        #print("summary_sentences", summary_sentences)
        #print("document_sentences", document_sentences)
        print("id_pair", id_pair)
        for i in range(len(summary_sentences)):
            id_sentence_summary = str(i+1) 
            for j in range(len(document_sentences)):
                id_sentence_summary = str(i+1) 
                id_sentence_document = str(j+1) 
                if not id_sentence_summary in self.__alignments[id_cluster]: self.__alignments[id_cluster][id_sentence_summary] = list()
                if mode == 1:
                    if self.__get_equals_words_atr(summary_sentences[i], document_sentences[j]) >= threshold:
                        self.__alignments[id_cluster][id_sentence_summary].append((id_pair, id_sentence_document))
                elif mode == 2:
                    if self.__get_relative_position_atr(i+1, j+1, len(summary_sentences), len(document_sentences)) >= threshold:
                        self.__alignments[id_cluster][id_sentence_summary].append((id_pair, id_sentence_document))
                else:
                    if self.__get_relative_size_atr(len(summary_sentences[i]), len(document_sentences[j])) >= threshold:
                        self.__alignments[id_cluster][id_sentence_summary].append((id_pair, id_sentence_document))
    
    def evaluate_together(self, thresholds):
        ''' Evaluate the alignment's set '''
        for id_cluster, cluster in self.__cluster_list.items():
            print("id_cluster", id_cluster)
            cluster.create_pairs()
            pair_list = cluster.get_pairs()
            self.__alignments[id_cluster] = dict()
            for id_pair, pair in pair_list.items():
                self.__evaluate_pairs_together(id_cluster, id_pair, pair, thresholds)
    
    def __evaluate_pairs_together(self, id_cluster, id_pair, pair, thresholds):
        ''' Evaluate the alignment between  a document and the summary '''
        summary_sentences = pair.get_raw_summary_sentences()
        document_sentences = pair.get_document_sentences()
        print("id_pair", id_pair)
        for i in range(len(summary_sentences)):
            id_sentence_summary = str(i+1) 
            for j in range(len(document_sentences)):
                id_sentence_summary = str(i+1) 
                id_sentence_document = str(j+1) 
                if not id_sentence_summary in self.__alignments[id_cluster]: self.__alignments[id_cluster][id_sentence_summary] = list()
                
                wo = self.__get_equals_words_atr(summary_sentences[i], document_sentences[j]) 
                rp = self.__get_relative_position_atr(i+1, j+1, len(summary_sentences), len(document_sentences)) 
                rz = self.__get_relative_size_atr(len(summary_sentences[i]), len(document_sentences[j]))
                
                if wo >= thresholds[0]  and rp >= thresholds[1]  and rz >= thresholds[2]:
                    self.__alignments[id_cluster][id_sentence_summary].append((id_pair, id_sentence_document))

          
    def __get_equals_words_atr(self, summary_sentence, document_sentence):
        ''' Return the proportions of equals words '''
        words_summary = utils.get_words(summary_sentence, stop_words=True)
        words_document = utils.get_words(document_sentence, stop_words=True)
        total_words = len(words_summary)
        equals_words = 0
        tmp_dict = dict()
        
        for word_summary in words_summary:
            for word_document in words_document:
                if word_summary == word_document and word_summary not in tmp_dict:
                    tmp_dict[word_summary] = 1
                    equals_words += 1            
            
        return equals_words / total_words
              
    def __get_relative_position_atr(self, position_summary, position_document, len_summary, len_document):
        ''' Return the relative position '''
        if len_document > len_summary:
            max_len = len_document
            min_len = len_summary
        else:
            max_len = len_summary
            min_len = len_document           

        division = max_len / min_len       
        
        windows_ceil = ceil(max_len / min_len)
        windows_floor = floor(max_len / min_len)      

        if (windows_ceil - division) < (division - windows_floor):
            windows = windows_ceil
        else:
            windows = windows_floor;

        if position_document > position_summary:
            max_pos = position_document
            min_pos = position_summary
        else:
            max_pos = position_summary
            min_pos = position_document
            
        relative_position = fabs(ceil(max_pos / windows) - min_pos) / (min_len - 1)

        if relative_position > 1.0:
            relative_position = 1.0

        return relative_position

    def __get_relative_size_atr(self, len_summary, len_document):
        ''' Return the relative size '''
        if len_document > len_summary:
            max_len = len_document
            min_len = len_summary
        else:
            max_len = len_summary
            min_len = len_document           
           
        relative_seize = (max_len - min_len) / max_len

        return relative_seize
    
    def get_baseline_alignments(self):
        return self.__alignments
      
    def print_data(self): 
        ''' Print the matrix's feature '''
        file = open("../resource/data/matriz.txt", "w")
        print(len(self.__manual_alignments), len(self.__equals_words_atr), len(self.__sense_units_atr), len(self.__cst_relations_atr), len(self.__type_cst_relations_atr), len(self.__relative_position_atr), len(self.__relative_size_atr))
        for key, value in self.__manual_alignments.items():
            print (key, value)
            file.write("%s, %s, %s, %s, %s, %s, %s, %s\n" %(key, self.__equals_words_atr[key], self.__sense_units_atr[key], self.__cst_relations_atr[key], self.__type_cst_relations_atr[key], self.__relative_position_atr[key], self.__relative_size_atr[key], value))
        file.close()  
   
    