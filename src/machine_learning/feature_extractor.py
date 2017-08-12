# -*- coding: utf-8 -*-
'''
Created on 25/09/2013

@author: roque
'''
import re
import utils
from math import floor, ceil, fabs
from cst.relations_cst import CSTRelations

type_relations = {
'Identity':'REDUNDANCIA', 'equivalence':'REDUNDANCIA', 'summary':'REDUNDANCIA', 'subsumption':'REDUNDANCIA', 'overlap':'REDUNDANCIA',
'historical background':'COMPLEMENTO', 'follow-up':'COMPLEMENTO', 'elaboration':'COMPLEMENTO',
'contradiction':'CONTRADICAO',
'citation':'FONTE', 'attribuition':'FONTE', 'modality':'FONTE',
'indirect speech':'ESTILO', 'translation':'ESTILO'}

class FeatureExtractor(object):
    '''
    Extracts the features for machine learning methods 
    '''

    def __init__(self, cluster_list, folder_cst_relations, manual_alignments):
        self.__cluster_list = cluster_list
        self.__manual_alignments = dict()
        self.__equals_words_atr = dict()
        self.__sense_units_atr = dict()
        self.__cst_relations_atr = dict()
        self.__type_cst_relations_atr = dict()
        self.__relative_position_atr = dict()
        self.__relative_size_atr = dict()
        self.__tep_synonyms = dict()
                
        cst = CSTRelations()
        self.__cst_alignments  = cst.read_relations_cst(folder_cst_relations, 'direct')
        self.__cst_complete_alignments  = cst.read_complete_relations(folder_cst_relations)
        self.__create_tep_synonyms() 
        self.__fill_manual_alignments(manual_alignments)
    
    def evaluate(self):
        ''' Evaluate the alignment's set '''
        for id_cluster, cluster in self.__cluster_list.items():
            print("id_cluster", id_cluster)
            cluster.create_pairs()
            pair_list = cluster.get_pairs()
            for id_pair, pair in pair_list.items():
                #print("id_pair", id_pair)
                self.__evaluate_pairs(id_cluster, id_pair, pair)
    
    def __evaluate_pairs(self, id_cluster, id_pair, pair):
        ''' Evaluate the alignment between  a document and the summary '''
        summary_sentences = pair.get_raw_summary_sentences()
        document_sentences = pair.get_document_sentences()
        #print("summary_sentences", summary_sentences)
        #print("document_sentences", document_sentences)
        print("id_pair", id_pair)
        for i in range(len(summary_sentences)):
            for j in range(len(document_sentences)):
                id_sentence = 'sumario_S' + str(i+1) + '__'  + id_pair + '_S' + str(j+1) 
                
                if not id_sentence in self.__manual_alignments: self.__manual_alignments[id_sentence] = 'nao' #label
                self.__equals_words_atr[id_sentence] = self.__get_equals_words_atr(summary_sentences[i], document_sentences[j])
                self.__sense_units_atr[id_sentence] = self.__get_sense_units_atr(summary_sentences[i], document_sentences[j])
                self.__cst_relations_atr[id_sentence] = self.__get_cst_relations_atr(id_cluster, id_pair, str(i+1), str(j+1))
                self.__type_cst_relations_atr[id_sentence] = self.__get_type_cst_relations_atr(id_cluster, id_pair, str(i+1), str(j+1))
                self.__relative_position_atr[id_sentence] = self.__get_relative_position_atr(i+1, j+1, len(summary_sentences), len(document_sentences))
                self.__relative_size_atr[id_sentence] = self.__get_relative_size_atr(len(summary_sentences[i]), len(document_sentences[j]))
                
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
            
        #if  equals_words == total_words: print("iguales", equals_words, total_words, words_summary, words_document)
        return equals_words / total_words
          
    def __get_sense_units_atr(self, summary_sentence, document_sentence):
        ''' Return the proportions of equals words'''
        words_summary = utils.get_words(summary_sentence, stop_words=True)
        words_document = utils.get_words(document_sentence, stop_words=True)
        #print("words_summary", words_summary)
        #print("words_sentence", words_sentence)
        unique_words = dict()
        cont = 0
        tmp = list()
        for word_summary in words_summary:
            if not word_summary in unique_words: # to avoid repetitions
                unique_words[word_summary] = 1
                for word_document in words_document:
                    if word_summary in self.__tep_synonyms and word_document in self.__tep_synonyms[word_summary]:
                        #print("synonyms", word_summary, word_sentence)
                        tmp.append((word_summary, word_document))
                        cont += 1
                
        return cont #(cont, tmp)
    
    def __get_cst_relations_atr(self, id_cluster, id_document, id_sentence_summary, id_sentence_document):
        ''' Return 1 if exist one relation between the sentences, 0 otherwise '''
        if id_sentence_summary in self.__cst_alignments[id_cluster]:
            if (id_document, id_sentence_document) in self.__cst_alignments[id_cluster][id_sentence_summary]:
                return 1
        return 0
    
    def __get_type_cst_relations_atr(self, id_cluster, id_document, id_sentence_summary, id_sentence_document):
        ''' Return the type of relation between the sentences(it can be REDUNDANCIA COMPLEMENTO CONTRADICAO FONTE ESTILO). 
            Return 'NOT_RELATION' otherwise '''
        if id_sentence_summary in self.__cst_alignments[id_cluster]:
            if (id_document, id_sentence_document) in self.__cst_alignments[id_cluster][id_sentence_summary]:
                #print(self.__cst_complete_alignments[id_cluster][id_sentence_summary])
                for type_relation, super_type in type_relations.items():
                    if (id_document, id_sentence_document, type_relation) in self.__cst_complete_alignments[id_cluster][id_sentence_summary]:
                        return super_type

        return 'NOT_RELATION'
           
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
    
    def __fill_manual_alignments(self, manual_alignments):
        ''' Identify the sentences with a manual alignments '''
        for summary_sentences in manual_alignments.values():
            for id_summary_sentence, document_sentences in summary_sentences.items():
                for tupla in document_sentences:
                    #print(id_summary_sentence, tupla[0], tupla[1])
                    self.__manual_alignments['sumario_S' + id_summary_sentence + '__'  + tupla[0] + '_S' + tupla[1]] = 'sim'

    def __create_tep_synonyms(self):
        ''' Create a synonyms dictionary using a TEP thesaurus '''
        file = open("../resource/lexical/base_tep2.txt", 'r', encoding='latin1')
        while True:
            line = file.readline()
            if not line: break
            tmp = re.match("(.*)\{(.+)\}(.*)", line).group(2)
            synonyms = [x.strip() for x in tmp.split(',')]

            for synonym in synonyms:
                if not synonym in self.__tep_synonyms: 
                    self.__tep_synonyms[synonym] =  [x for x in synonyms if x != synonym]
                else:
                    self.__tep_synonyms[synonym] += [x for x in synonyms if x != synonym and not x in self.__tep_synonyms[synonym]]
        
        file.close()  
    
        
    def print_data(self, file_name): 
        ''' Print the matrix's feature '''
        file = open(file_name, "w")
        print(len(self.__manual_alignments), len(self.__equals_words_atr), len(self.__sense_units_atr), len(self.__cst_relations_atr), len(self.__type_cst_relations_atr), len(self.__relative_position_atr), len(self.__relative_size_atr))
        for key, value in self.__manual_alignments.items():
            print (key, value)
            file.write("%s, %s, %s, %s, %s, %s, %s, %s\n" %(key, self.__equals_words_atr[key], self.__sense_units_atr[key], self.__cst_relations_atr[key], self.__type_cst_relations_atr[key], self.__relative_position_atr[key], self.__relative_size_atr[key], value))
        file.close()  
        