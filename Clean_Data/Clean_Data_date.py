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
                l0 = loan_amount_preprocess0(data)
            except:
                l0 = None
            l1 = loan_amount_preprocess1(data)
            try:
                c = country_preprocess(data)
            except:
                c = None
            di= pd.DataFrame([data,l1,l0,c,len(data)],index=['raw_text','re_loan_amount','loan_amount','country','num_char'],columns=[DIR[i]]).T
            raw_df_lst.append(di)
    #print(len(raw_df_lst))
    df_raw = pd.concat(raw_df_lst)
    return df_raw
    
    
    
    
def date_preprocess(text):
    '''Grab Date'''
    return
    
    
def txt_to_csv(path,out_path):
    '''Input path is path for all text files, output path is path to output
    file'''
    df_raw = txt_to_df(path)
    return df_raw.to_csv(out_path,index=False)


#def main():
#    return

#if __name__ == "__main__":
#    main()
