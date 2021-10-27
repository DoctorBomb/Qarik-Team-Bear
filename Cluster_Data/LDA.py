#! /usr/bin/env python3

from itertools import *
import numpy as np
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from gensim import corpora, models
import gensim
import _pickle as cPickle
from sklearn.externals import joblib
import bz2
import pyLDAvis
import pyLDAvis.gensim



## Path to text files
path = "/home/kbari/git_repo/FinanceErdosProj/PyMuPdf_Text/"
path1 = "/home/kbari/git_repo/FinanceErdosProj/Tesseract_Text/"

## Load from txt from files to a dataframe; Other information to include possibly?

#pd.read_table(file,header=None,quotechar=None,quoting=3,error_bad_lines=False) for file in DIR]
def txt_to_df(path):
    ''' Put all txt files into single dataframe'''
    DIR = os.listdir(path)
    raw_df_lst = []
    for i in range(len(DIR)):
        with open(path+DIR[i],encoding = "ISO-8859-1") as f:
            lines = f.readlines()
            data = '\n'.join(map(str,lines))
            print(DIR[i])
            di= pd.DataFrame([data,len(data)],index=['raw_text','num_char'],columns=[DIR[i]]).T
            raw_df_lst.append(di)
    #print(len(raw_df_lst))
    df_raw = pd.concat(raw_df_lst)
    return df_raw


df = txt_to_df(path)
df1 = txt_to_df(path1)
dF = pd.concat([df,df1])


tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
p_stemmer = PorterStemmer()

def text_preprocess(text):
	tokens = tokenizer.tokenize(text.lower())
	t = [i for i in tokens if not i in en_stop]	
	t1 = [p_stemmer.stem(i) for i in t]
	return t1

#T = [ text_preprocess(t) for t in dF.raw_text]

