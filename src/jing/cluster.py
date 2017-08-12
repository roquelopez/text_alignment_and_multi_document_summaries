# -*- coding: utf-8 -*-
'''
Created on 17/07/2013

@author: roque
'''

from jing.pair import Pair
from jing.hmm import HMM
from jing.viterbi import viterbi
from utils import stop_words_list

class Cluster(object):
    '''
    Represents a summary and the original documents 
    '''

    def __init__(self, stop_words=True):
        self.__document_list = dict()
        self.__summary = ""# summary text
        self.__pair_list = dict()# list of each document with the summary
        self.__alignment = dict()
        self.__stop_words = dict()# stopwords list
        if stop_words:# verify if is necessary a stopwords filter
            self.__stop_words = stop_words_list()
    
    def add_summary(self, summary):
        ''' Adds the summary '''
        self.__summary = summary
    
    def add_document(self, document_name, text):
        ''' Adds a document '''
        self.__document_list[document_name] = text
    
    def get_summary(self):
        ''' Returns the summary '''
        return self.__summary
    
    def get_document_list(self):
        ''' Returns the document list '''
        return self.__document_list
    
    def get_alignment(self):
        ''' Returns the alignment '''
        return self.__alignment
    
    def get_pairs(self):
        ''' Returns the pairs list '''
        return self.__pair_list
    
    def create_pairs(self):
        ''' Creates a pair(document with the summary) '''
        for name, text in self.__document_list.items():
            p = Pair()
            p.create_sentence_list(self.__summary, text)
            p.create_position_list()
            self.__pair_list[name] = p
    
    def create_hmms(self):
        ''' Creates a Hidden Markov Model for each summary sentence for the document list '''
        for name, pair in self.__pair_list.items():
            print(" Document", name) 
            paths = dict()
            for id_sentence, sentence_summary in pair.get_clean_summary_sentences():
                hmm = HMM(sentence_summary, pair.get_position_word_list())
                hmm.create_hmm()
                path = viterbi(hmm.get_observations(), hmm.get_states(), hmm.get_start_probability(), hmm.get_transition_probability(), hmm.get_emission_probability(), pair.get_position_word_list())[1]
                paths[id_sentence] = path
                self.__create_alignment(id_sentence, name, path, pair.get_position_word_list())
                           
            self.__create_sentences_format(pair, paths)
    
    def __create_alignment(self, id_sentence, id_document, path, position_word_list):
        ''' Creates the alignment for a sentence summary '''    
        real_id = str(id_sentence + 1)
        if not real_id in self.__alignment: self.__alignment[real_id] = list()
        sentences = dict()
        for position in path:
            sentence_position = position.split('_')[0]
            word = self.__get_word(position, position_word_list)

            if not word in self.__stop_words:
                sentences[sentence_position] = None

        for sentence_position in sentences:
            self.__alignment[real_id].append((id_document, sentence_position))
    
    def __get_word(self, position, tmp_list):
        ''' Returns the word of a given position '''
        for key, value in tmp_list.items():
            if position in value: 
                return key
 
    def __create_sentences_format(self, pair, paths):
        ''' Creates the format for all sentences summary '''
        sentences = pair.get_raw_summary_sentences()

        for id_sentence in range(len(sentences)):
            if id_sentence in paths:
                text = self.__create_sentence_format(sentences[id_sentence], paths[id_sentence], pair.get_position_word_list())
                print(text)
            else:
                print(sentences[id_sentence])
            
    def __create_sentence_format(self, sentence_summary, path, words_selected):
        ''' Creates the format for one sentence summary '''
        sentence_summary = sentence_summary.split(" ")
        result = ""
        tmp = '-'
        nro = '+'
        i = 0
        for word in sentence_summary:
            if word in words_selected and not word in self.__stop_words:
                nro = path[i].split('_')[0]
                if nro == tmp:
                    result += ' '+word
                else:
                    if tmp == '-':
                        result += ' S'+nro+'('+word
                    else:
                        result += ') S'+nro+'('+word
                    tmp = nro 
                i += 1                  
                
            else:
                if tmp == '-':
                    result += ' '+ word
                else:
                    result += ') '+ word
                tmp = '-'
                
        if nro == tmp:
            result += ')'
        return result[1:]
