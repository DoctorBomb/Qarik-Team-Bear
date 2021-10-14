#! /usr/bin/env python3

from itertools import *
import numpy as np
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')

#nltk.download()


## Path to text files
path = "/home/kbari/Documents/Erdos/pdfminer_texts/"

## Load from txt from files to a dataframe; Other information to include possibly?
def txt_to_df(path):
    ''' Put all txt files into single dataframe'''
    DIR = os.listdir(path)
    raw_df_lst = []
    #pd.read_table(file,header=None,quotechar=None,quoting=3,error_bad_lines=False) for file in DIR]
    for i in range(len(DIR)):
        with open(DIR[i]) as f:
            lines = f.readlines()
            data = '\n'.join(map(str,lines))
            di = pd.DataFrame([data,len(data)],index=['raw_text','num_char'],columns=[DIR[i]]).T
            raw_df_lst.append(di)
    #print(len(raw_df_lst))
    df_raw = pd.concat(raw_df_lst)
    return df_raw



## Removes punctuation, stopwords, lemmatizes
def text_preprocess(text):
    '''
    Remove all punctuation,stopwords, lemmatize -> returns list of words
    '''
    stemmer = WordNetLemmatizer()
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join([i for i in nopunc if not i.isdigit()])
    nopunc =  [word.lower() for word in nopunc.split() if word not in stopwords.words('english')]
    return [stemmer.lemmatize(word) for word in nopunc]
