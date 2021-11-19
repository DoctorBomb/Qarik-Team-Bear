#! /usr/bin/env python3

from itertools import *
import os
import numpy as np
import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
#nltk.download()

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
            try:
                c = proj_name_preprocess(data)
                n = int(len(c))
            except:
                c = None
                n = int(0)
            di= pd.DataFrame([data,c,n],index=['raw_text','proj_name','num_char'],columns=[DIR[i]]).T
            raw_df_lst.append(di)
    #print(len(raw_df_lst))
    df_raw = pd.concat(raw_df_lst)
    return df_raw
    
def proj_name_preprocess(text):
    start = 'agreement'
    start1 = 'number'
    end = 'between'
    end1 = 'among'
    t = text.lower().split(start)[1].split(end)[0].strip()
    s = text.lower().split(start1)[1].split(end)[0].strip()
    r = text.lower().split(start)[1].split(end1)[0].strip()
    if 'date' in t:
        if 'date' in s:
            if 'date' in r:
                return None
            else:
                return r
        else:
            return s
    else:
        return t
    #reg_ex = 'loan[\S\n ]*?between[\S\n ]*?([\S\n ]+?\(.+?\d+?\))'
    #return re.search(reg_ex,text.lower())


df = txt_to_df(path)
df1 = txt_to_df(path1)
dF = pd.concat([df,df1])
dG = dF.proj_name
dL = dF.num_char
dl = dG[dF.num_char >350]

#def see(dG,i,j):
#    for k in range(i,j):
#        print(k,dG[k])

