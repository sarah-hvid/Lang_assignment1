"""
A script that performs a collocation analysis based on the mutual information score.
"""
# System tools
import os
import sys
import argparse
import glob

# Data analysis
import pandas as pd
import collections
import itertools
import math

# Text analysis
import re
import spacy
from spacy.tokens import Span

# set nlp parameters
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 1700000 


def parse_args():
    '''
    Function that specifies the available user arguments.
    '''
    # Initialise argparse
    ap = argparse.ArgumentParser()
    
    # command line parameters
    ap.add_argument("-f", "--file_input", required = True, help = "The filename or directory we want to work with.")
    ap.add_argument("-st", "--search_term", required = True, help = "The search term/focus word to find collocates for.")
    ap.add_argument("-o", "--output_type", required = False, default = 'separate', help = "The output type you want when inputting a directory; 'separate' for a dataframe for each file, 'gathered' for a dataframe that contains results for al files.")
    ap.add_argument("-wi", "--window", required = False, default = 5, help = "The window to find collocates within.", type = int)

    args = vars(ap.parse_args())
    return args


def read_data(filepath):
    '''
    Function that reads text data and cleans the filename.
    
    filepath: a path to a text file
    '''
    with open(filepath, 'r') as f:
        text = f.read()
    
    filename = filepath.split("/")[-1]
    filename = filename.split(".")[0]
    return text, filename


def preprocess_data(text_input):
    '''
    Function that preprocesses text data by lowercasing and removing puncts. It then creates a spacy doc object. 
    
    text_input: a text object
    '''
    # lowercasing the text and removing puncts. 
    text_lower = text_input.lower() 
    text_no_punct = re.sub('\W+','', text_lower)
    
    # creating doc for tokenization
    doc = nlp(text_no_punct, disable=["tok2vec", "tagger", "parser", "lemmatizer", "NER"]) 
    return doc


def calc_MI(A, B, AB, span, corpus_size):
    '''
    Function that contains the MI score formula.
    
    A: frequency of key word
    B: frequency of collocate word across the corpus
    AB: frequency of word as collocate
    span: the span of the collocates to either side of the key word
    corpus_size: number of words in the corpus
    '''
    score = math.log10((AB * corpus_size) / (A * B * span)) / math.log10(2)
    return score


def calculate_metrics(doc, key_word, window, file_name):
    '''
    Function that calculates the MI metrics and the MI score for a corpus. The key values are returned as tuples in a list.
    
    doc: a spacy text object
    key_word: the word we want to find collocates for.
    window: the window of interest to either side of the key word.
    file_name: the name of the file we are working with
    '''
    # initialize corpus and key word counter
    corpus_size = 0
    A = 0
    
    # initialize word and collocates count
    words_list = []
    collocate_list = []
    
    for token in doc:
        corpus_size += 1 # corpus size counter
        words_list.append(str(token))

        if token.text == key_word:
            # getting a hold of the collocate words
            index_key = token.i
            left_window = Span(doc, token.i - window, token.i)
            
            for token in left_window:
                collocate_list.append(str(token))

            right_window = Span(doc, index_key + 1, index_key + window + 1)
            for token in right_window:
                collocate_list.append(str(token))

            A += 1 # frequency of key word     
            span = window * 2 # number of words in the window

    # counting occurences across the input text and across the collocate list
    words_count = collections.Counter(words_list)
    collocate_count = collections.Counter(collocate_list)
    
    output_data = []
    # looping through the dictionaries to get the values for the MI calculation
    for key, value in collocate_count.items():
        AB = value # frequency of word as collocate
        
        if key in words_count:
            B = words_count[key] #frequency of collocate word across input text
            #calculating the MI score
            MI = calc_MI(A, B, AB, span, corpus_size) 
        
        output_data.append((file_name, key_word, window, key, AB, B, MI))
    return output_data


def collocate_df(output_data, file_name, keyword):
    '''
    Function that creates a dataframe of the results for each file sorted by MI score and saves it as a CSV file
    
    output_data: a list of tuples
    file_name: the name of the file we are working with
    keyword: the input keyword to find collocates for
    '''
    df = pd.DataFrame(output_data, 
                      columns = ['file_name','key_word', 'window', 'collocate_term', 'collocate_frequency', 'text_frequency', 'MI_score'])
    df.sort_values(by=['MI_score'], inplace = True, ascending = False) 
    df.to_csv(F"output/MI_{file_name}_{keyword}.csv", index = False)
    return
    

def collocate_all_df(joined_paths, keyword, window):
    '''
    Function that either creates several dataframe outputs per file, or a gathered dataframe containing all results per file dependent on user input.
    
    joined_paths: an iterable of paths to all the files in the specified directory
    keyword: the input keyword to find collocates for
    window: the window of interest to either side of the key word.
    '''
    # parse arguments
    args = parse_args()
    output_type = args['output_type']
    out_list = []
    
    # creating variables for status prints
    counter = 1
    num_files = len(joined_paths)
    # calculate MI for each file in the dir
    for file in joined_paths:
        text, file_name = read_data(file)
        print(f'[INFO] Processing file {counter} of {num_files}')
        doc = preprocess_data(text)
        output_data = calculate_metrics(doc, keyword, window, file_name) # create output data
        counter += 1
        
        # write to output for each file
        if output_type == 'separate':
            collocate_df(output_data, file_name, keyword)
            
        # appending the output data to the out_list for each file
        if output_type == 'gathered':
            out_list.append(output_data)
    
    if output_type == 'gathered':
        out_list = itertools.chain(*out_list) # unnesting the list
        
        # write the gathered CSV to output
        df = pd.DataFrame(out_list, 
                          columns = ['file_name', 'key_word', 'window', 'collocate_term', 'collocate_frequency', 'text_frequency', 'MI_score'])
        df.to_csv(f'output/MI_all_{keyword}.csv', index = False)
    return

   
def main():
    '''
    The process of the script.
    '''
    # parse arguments
    args = parse_args()
    
    input_name = args['file_input']
    keyword = args['search_term']
    window = args['window']

    # if path provided is a file:
    isFile = os.path.isfile(input_name)
    if isFile == True:
        print('[INFO] Input is a file')
        text, file_name = read_data(input_name)
        doc = preprocess_data(text)
        output_data = calculate_metrics(doc, keyword, window, file_name)
        collocate_df(output_data, file_name, keyword)
        
        print('[INFO] Script success.')

    # if path is a directory:
    isDirectory = os.path.isdir(input_name)
    if isDirectory == True:
        print('[INFO] Input is a directory')
        joined_paths = glob.glob(os.path.join(input_name, '*.txt'))

        print('[INFO] Collocation analysis ...')
        collocate_all_df(joined_paths, keyword, window)

        print('[INFO] Script success.')
                

if __name__ == '__main__':
    main()    
