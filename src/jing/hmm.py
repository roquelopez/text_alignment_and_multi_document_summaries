# -*- coding: utf-8 -*-
'''
Created on 19/07/2013

@author: roque
'''
from settings import CONST, P1, P2, P3, P4, P5, P6
 
class HMM(object):
    '''
    Represents a Hidden Markov Model 
    '''

    def __init__(self, words_sentence_sum, position_word_list):
        self.__probability_list = [None] * len(words_sentence_sum)
        self.__words_sentence_sum = words_sentence_sum
        self.__position_word_list = position_word_list
        
        self.__states = list()# Position of the words summary in the document
        self.__observations = words_sentence_sum# Words of the summary
        self.__start_probability = dict()# Equal for all positions of the first word of the summary
        self.__transition_probability = dict()# Probability of going from word[i] to word[i+1]
        self.__emission_probability = dict()# Probability of going from one position a one word, always is 1      
                
    def create_hmm(self):
        ''' Calculates the Hidden Markov Model component: states, start, transition and emission probability ''' 
        self.__calculate_start_probability()
        
        for i in range(len(self.__words_sentence_sum) - 1):
            self.__calculate_transition_probability(i+1, self.__words_sentence_sum[i], self.__words_sentence_sum[i+1])

        self.__calculate_states()
        self.__calculate_emission_probability()
    
    def __calculate_start_probability(self):
        ''' Calculates the probability for the first word summary, is equal for all positions '''             
        probability = 1 / len(self.__position_word_list[self.__words_sentence_sum[0]])

        for position in self.__position_word_list[self.__words_sentence_sum[0]]:
            self.__start_probability[position] = probability 
            
    def __calculate_transition_probability(self, index, previous_word, word):
        ''' Calculates the probabilities for each position ''' 
        for position_w in self.__position_word_list[word]:
            S2 = int(position_w.split('_')[0])# S2 = position of the sentence
            W2 = int(position_w.split('_')[1])# W2 = position of word in the sentence
            max_prob = -1

            for position_bw in self.__position_word_list[previous_word]:
                S1 = int(position_bw.split('_')[0])
                W1 = int(position_bw.split('_')[1])
                
                if S1 == S2 and W1 == W2 - 1:# P1
                    max_prob = P1
                    
                elif S1 == S2 and W1 < W2 - 1:# P2
                    max_prob = P2
                
                elif S1 == S2 and W1 > W2:# P3
                    max_prob = P3
                    
                elif S2 - CONST < S1 < S2:# P4
                    max_prob = P4
                    
                elif S2 < S1 < S2 + CONST:# P5
                    max_prob = P5
                    
                elif abs(S2 - S1) >= CONST:# P6
                    max_prob = P6
                    
                if not position_bw in self.__transition_probability:
                    self.__transition_probability[position_bw] = dict()
                self.__transition_probability[position_bw][position_w] = max_prob

    def __calculate_states(self):
        ''' Calculates the states, e.g. [the, people, works] '''            
        for state in self.__transition_probability.keys():
            self.__states.append(state)
            
        for state in self.__start_probability:
            if not state in self.__transition_probability.keys():
                self.__states.append(state)
                #print("New word")
    
    def __calculate_emission_probability(self): 
        ''' Calculates the emission probability, e.g. '1_7':{'people':1.0} '''
        for word in self.__words_sentence_sum:          
            for position in self.__position_word_list[word]:
                self.__emission_probability[position] = {word:1.0}
                 
    def get_observations(self):
        ''' Returns the observations list '''
        return self.__observations
    
    def get_states(self):
        ''' Returns the states list '''
        return self.__states 
    
    def get_start_probability(self):
        ''' Returns the start probability list '''
        return self.__start_probability
    
    def get_transition_probability(self):
        ''' Returns the transition probability list '''
        return self.__transition_probability
    
    def get_emission_probability(self):
        ''' Returns the emission probability list '''
        return self.__emission_probability                  
      
    def print_probabilities(self):
        print("start probability",self.__words_sentence_sum[0], self.__start_probability)  
        print("states", self.__states) 
        print("emission pobability", self.__emission_probability)
        #print("transition probability", self.__transition_probability)