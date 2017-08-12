# -*- coding: utf-8 -*-
'''
Created on Aug 2, 2013

@author: roque
'''

class Evaluator(object):
    '''
    Evaluates the performance of the automatic alignments 
    '''

    def __init__(self):
        self.__correct_alignment = 0
        self.__real_alignments = 0
        self.__predicted_alignments = 0
        self.__recall_accumulative = 0
        self.__precision_accumulative = 0
        self.__recall_average = 0
        self.__precision_average = 0
        
        self.__total_type = dict()
        self.__correct_type = dict()
        
        self.__not_alignments = dict()
        self.__errors = 0 # By Veronica
    
    def create_not_alignments(self, cluster_list, manual_alignments):
        for id_cluster, cluster in cluster_list.items():
            #print("id_cluster", id_cluster)
            cluster.create_pairs()
            pair_list = cluster.get_pairs()
            if id_cluster not in self.__not_alignments: self.__not_alignments[id_cluster] = dict()
            
            for id_pair, pair in pair_list.items(): 
                summary_sentences = pair.get_raw_summary_sentences()
                document_sentences = pair.get_document_sentences()

                for i in range(len(summary_sentences)):
                    id_sent_summ = str(i+1)
                    if id_sent_summ not in self.__not_alignments[id_cluster]: self.__not_alignments[id_cluster][id_sent_summ] = list()
                    for j in range(len(document_sentences)):
                        if id_sent_summ in manual_alignments[id_cluster] and not self.has_alignment(manual_alignments[id_cluster][id_sent_summ], id_pair, str(j+1)):
                            self.__not_alignments[id_cluster][id_sent_summ].append((id_pair, str(j+1)))
        #print(self.__not_alignments)
    
    def has_alignment(self, manual_alignments, id_doc, id_sentence):   
        #print(manual_alignments)
        for m_id_doc, m_id_sentence, id_type in manual_alignments:
            if m_id_doc == id_doc and m_id_sentence == id_sentence:
                return True
            
        return False
            
    def evaluate_accumulative(self, manual_result, automatic_result):
        ''' Evaluates the alignments performance, use the sum of partial alignments(correct, real and predicted) '''     
        clusters = manual_result.keys()
        for cluster in clusters:
            manual_sentences = manual_result[cluster]
            automatic_sentences = automatic_result[cluster] if cluster in automatic_result else {}
            sentences = manual_sentences.keys()
            for id_sentence in sentences:
                #print('sentence', id_sentence)
                self.__fill_alignments_type(manual_sentences[id_sentence])
                if id_sentence in automatic_sentences:
                    self.__verify(manual_sentences[id_sentence], automatic_sentences[id_sentence])
                else:
                    self.__real_alignments += len(manual_sentences[id_sentence])
        
        
    def evaluate_average(self, manual_result, automatic_result):
        ''' Evaluate the alignments performance, use the average of precision, recall and F-measure '''
        print(automatic_result)
        clusters = sorted(manual_result.keys())

        for cluster in clusters:
            self.__correct_alignment = 0
            self.__real_alignments = 0
            self.__predicted_alignments = 0
        
            manual_sentences = manual_result[cluster]
            automatic_sentences = automatic_result[cluster] if cluster in automatic_result else {}
            sentences = manual_sentences.keys()
            for id_sentence in sentences:
                #print('sentence', id_sentence)
                self.__fill_alignments_type(manual_sentences[id_sentence])
                if id_sentence in automatic_sentences:
                    self.__verify(manual_sentences[id_sentence], automatic_sentences[id_sentence])
                else:
                    self.__real_alignments += len(manual_sentences[id_sentence])
            self.__recall_average += self.get_recall()
            self.__precision_average += self.get_precision()
            ###self.get_recall()
            ###self.get_precision()
            ###print(cluster, self.get_fmeasure())
        self.__recall_average /= len(clusters)
        self.__precision_average /= len(clusters)
                             
    def __verify(self, manual_alignments, automatic_alignments):
        ''' Verifies if the  manual are equal to the automatic alignments '''
        self.__real_alignments += len(manual_alignments)
        self.__predicted_alignments += len(automatic_alignments)
        
        for m_name, m_sentence, id_type in manual_alignments:
            if id_type not in self.__correct_type: self.__correct_type[id_type] = 0
            not_in = True
            for a_name, a_sentence in automatic_alignments:
                if m_name == a_name and m_sentence == a_sentence:# manual_alignment == automatic_alignment:
                    ##print(m_name, a_name, m_sentence, a_sentence)
                    self.__correct_alignment += 1
                    self.__correct_type[id_type] += 1
                    not_in = False
            
            if not_in:
                self.__errors += 1
                
    def __fill_alignments_type(self, manual_alignments):
        for m_name, m_sentence, id_type in manual_alignments:
            if id_type not in self.__total_type: self.__total_type[id_type] = 0
            self.__total_type[id_type] += 1 
                 
    def get_precision(self):
        ''' Returns the precision '''
        if self.__predicted_alignments == 0:
            return 0
        self.__precision_accumulative = self.__correct_alignment / self.__predicted_alignments
        return self.__precision_accumulative
    
    def get_recall(self):
        ''' Returns the recall '''
        if self.__real_alignments == 0:
            return 0
        self.__recall_accumulative = self.__correct_alignment / self.__real_alignments
        return self.__recall_accumulative
    
    def get_fmeasure(self):
        ''' Returns the F-measure '''
        return (2 * self.__precision_accumulative * self.__recall_accumulative) / (self.__precision_accumulative + self.__recall_accumulative)
    
    def restart(self):
        ''' Restart the data '''
        self.__correct_alignment = 0
        self.__real_alignments = 0
        self.__predicted_alignments = 0
        self.__recall_accumulative = 0
        self.__precision_accumulative = 0
        self.__recall_average = 0
        self.__precision_average = 0
    
    def ver_measure(self, ):
        not_alignments = 0
        for cluster, sentences in self.__not_alignments.items():
            for alignments in sentences.values():
                not_alignments += len(alignments)

        total = self.__real_alignments + not_alignments
        tmp = self.__real_alignments - self.__correct_alignment
        final = total - (tmp + self.__errors)
        print("%s   %s of %s" % (float(final) / float(total), final, total))
        
    def print_measures(self):
        if self.__precision_average == 0:# mode accumulative 
            print('corrects', self.__correct_alignment)
            print('real', self.__real_alignments)
            print('predicted', self.__predicted_alignments)
            
            print("precision accumulative ", self.get_precision())
            print("recall accumulative ", self.get_recall())
            print("f measure accumulative ", self.get_fmeasure())
        else:# mode average
            print("precision average", self.__precision_average)
            print("recall average", self.__recall_average)
            self.__precision_accumulative = self.__precision_average
            self.__recall_accumulative = self.__recall_average
            print("f measure average", self.get_fmeasure())            