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


def loan_amount_preprocess(text):
    '''Grab loan amount'''
    return

def loan_amount_preprocess1(text): 
    ''' Grab Loan amount using reg exp'''
    start = 'ARTICLE II' 
    end =  'ARTICLE III'
    try:
        t1 = (text.split(start)[1].split(end)[0])
        r = re.search("\((.+?)\)",t1).group(1)
        #print('r=',r)
        if contains_number(r):
            return r
    except:
        pass
    try:
        t1 = (text.split(start)[1].split(end)[0])
        r = re.findall("\$.+?\s",t1)[0]
        if contains_number(r):
            return r
    except:
        pass
    start = 'ARTICLE H'
    end =  'ARTICLE III'
    try:
        t1 = (text.split(start)[1].split(end)[0])
        r1 = re.search("\((.+?)\)",t1).group(1)
        #print('r1=',r1)
        if contains_number(r1):
            return r1
    except:
        pass
    start = 'ARTICLE H'
    end =  'ARTICLE M'
    try:
        t1 = (text.split(start)[1].split(end)[0])
        r2 = re.search("\((.+?)\)",t1).group(1)
        #print('r2=',r2)
        if contains_number(r2):
            return r2
    except:
        pass
    start = 'ARTICLE II'
    end =  'ARTICLE M'
    try:
        t1 = (text.split(start)[1].split(end)[0])
        r3 = re.search("\((.+?)\)",t1).group(1)
        #print('r3=',r3)
        if contains_number(r3):
            return r3
    except:
        pass
    
    
def contains_number(reg_exp):
    y = [char.isdigit() for char in reg_exp]
    if y.count(True) > 5:
        return True
    return False

def loan_amount_preprocess0(text):
    ''' Grab Loan amount '''
    start = 'ARTICLE II'
    end =  'ARTICLE III'
    t1 = (text.split(start)[1].split(end)[0])
    t = [s.translate(str.maketrans('','',string.punctuation)) for s in t1.split()]
    n = [int(i) for i in t if i.isdigit()]
    n = [i for i in n if i%100000 == 0]
    return max(n)
    
def txt_to_csv(path,out_path):
    '''Input path is path for all text files, output path is path to output
    file'''
    df_raw = txt_to_df(path)
    return df_raw.to_csv(out_path,index=False)


#def main():
#    return

#if __name__ == "__main__":
#    main()
