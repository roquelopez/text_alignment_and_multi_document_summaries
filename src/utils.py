# -*- coding: utf-8 -*-
'''
Created on 17/07/2013

@author: roque
'''
import re
import shutil
import os
from bs4 import BeautifulSoup

def get_words(text, stop_words=False):
    ''' Returns a word list of a text '''
    if stop_words:
        stop_list = stop_words_list()
        return [x for x in re.split("\s+", text) if len(x) > 0 and x not in stop_list]
    else:
        return [x for x in re.split("\s+", text) if len(x) > 0]
        

def read_file(file_path):
    ''' Get the text of a file '''
    my_file = open(file_path,"r",encoding='latin1')#, errors='ignore')
    text = my_file.read()
    my_file.close()
    return text 

def clear_text(text):
    ''' Removes special symbols of text '''
    text = text.replace(',', '')
    text = text.replace('.', '')
    text = text.lower()
    return text

def stop_words_list():
    ''' Creates a list of stopwords '''
    my_list = dict()
    file = open("../resource/lexical/stopwords_portugues.txt", 'r', encoding='latin1')
    while True:
        line = file.readline()
        if not line: break
        my_list[line.strip()] = None
    file.close()
    return my_list

def copy_files():
    ''' Copy a list of files and rename them '''
    root = "../resource/data/CSTNews/"
    new_root = "../resource/data/new_CSTNews/"
    
    for folder in os.listdir(root):
        destination = os.path.join(new_root, folder)
        os.makedirs(destination)
        partial_source = os.path.join(root, folder, 'CST')
        file_name = ''.join([x for x in os.listdir(partial_source) if x.startswith('Cluster')])
        source = os.path.join(partial_source, file_name)

        shutil.copy(source, destination)
        #rename
        file1 = os.path.join(destination, file_name)
        file2 = os.path.join(destination, 'Releçoes_Textos.xml')
        os.rename(file1, file2)
        
def rename_files_xml_data():
    ''' Rename a list of files with the names from the  xml file'''
    folder_path = "../resource/data/cstnews_corpus_renamed/"
    new_names = "../resource/data/manual_alignments/"
    list_names = dict()
    for file in os.listdir(new_names):
        text_document = read_file(os.path.join(new_names, file))
        soup = BeautifulSoup(text_document)
         
        for doc in soup.findAll('doc'):
            name = doc.get('name')
            tmp_list = name.split('_')
            new_name = tmp_list[1]+'_'+tmp_list[0]+'.txt.seg'
            if not new_name in list_names:
                list_names[new_name] = name
            print(new_name, name)   
    print("Size list", len(list_names))

    for file in os.listdir(folder_path):
        if file in list_names:
            file1 = os.path.join(folder_path, file)
            file2 = os.path.join(folder_path, list_names[file])
            print(file1, file2)
            os.rename(file1, file2)
   
def rename_files():
    ''' Rename a list of files '''
    root_path = "../resource/data/CSTNews_original/"
    
    for folder in os.listdir(root_path):
        final_path = os.path.join(root_path, folder, 'Textos-fonte segmentados')
        for file_name in os.listdir(final_path):
            file1 = os.path.join(final_path, file_name)
            file2 = os.path.join(final_path, file_name.replace('.seg', ''))
            os.rename(file1, file2)
