# -*- coding: utf-8 -*-
'''
Created on 18/07/2013

@author: roque
'''
import utils
from settings import SPLITTER_SENTENCE

class Pair(object):
    '''
    Represents a summary and a original document in a clean format
    '''

    def __init__(self):
        self.__document_sentence_list = list()# sentence list of the document
        self.__summary_sentence_list = list()# sentence list of the summary
        self.__position_word_list = dict()# position of the words summary in the document
        self.__unique_words_summary = dict()# unique words of the summary 
        self.__words_summary = list()# word list of the summary
    
    def create_sentence_list(self, summary_text, document_text):
        ''' Divides the summary and document text in a list of sentences '''
        summary_text = utils.clear_text(summary_text)
        document_text = utils.clear_text(document_text)
        self.__document_sentence_list = [x for x in document_text.split(SPLITTER_SENTENCE) if len(x) > 0] #document_text.split(SPLITTER_SENTENCE)
        self.__summary_sentence_list = [x for x in summary_text.split(SPLITTER_SENTENCE) if len(x) > 0] #summary_text.split(SPLITTER_SENTENCE)
        self.__get_words_summary(summary_text)
        
    def create_position_list(self):
        ''' Obtains the positions in the document of the words summary: 'S1_W1'
        S1 = position of the sentence, W1 = position of word in the sentences '''
        for i in range(len(self.__document_sentence_list)):
            words = utils.get_words(self.__document_sentence_list[i])
            for j in range(len(words)):
                if words[j] in  self.__unique_words_summary:
                    if not words[j] in self.__position_word_list:
                        self.__position_word_list[words[j]] = list()
                    self.__position_word_list[words[j]].append(str(i+1)+'_'+str(j+1))
      
    def __get_words_summary(self, summary_text):
        ''' Gets unique words of the summary '''
        self.__words_summary = utils.get_words(summary_text)
        for word in self.__words_summary:
            if word in self.__unique_words_summary:
                self.__unique_words_summary[word] += 1
            else:
                self.__unique_words_summary[word] = 1
    
    def get_clean_summary_sentences(self):
        ''' Gets only sentences of the summary with words in the document '''
        clean_sentences = dict()
        id_cont = 0
        for sentence in self.__summary_sentence_list:
            words_in_document = self.__get_words_in_document(sentence)
            if len(words_in_document) > 0:
                clean_sentences[id_cont] = words_in_document
            id_cont += 1
        return clean_sentences.items()
    
    def get_raw_summary_sentences(self):
        ''' Gets all sentences of the summary '''
        return self.__summary_sentence_list
    
    def get_document_sentences(self):
        ''' Gets all sentences of the document '''
        return self.__document_sentence_list
    
    def __get_words_in_document(self, sentence_summary):
        ''' Gets a words list of a text '''
        words = sentence_summary.split(' ')
        new_words = list()
        for word in words:
            if word in self.__position_word_list:
                new_words.append(word)

        return new_words          
         
    def get_position_word_list(self):
        ''' Returns the positions list '''
        return self.__position_word_list
        
    def print_pair(self):
        for word, positions in self.__position_word_list.items():
            print(word)
            print(positions)