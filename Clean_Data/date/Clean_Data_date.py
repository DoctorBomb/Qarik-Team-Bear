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
path = "/Users/bingjinliu/Desktop/Erdos Institute/project/Data_txt/"
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
                d = date_preprocess(DIR[i])
            except:
                d = None
            
            try:
                s = sector_preprocess(DIR[i])
            except:
                s = None

            di= pd.DataFrame([data,d,s,len(data)],index=['raw_text','date','sector','num_char'],columns=[DIR[i]]).T
            raw_df_lst.append(di)
    #print(len(raw_df_lst))
    df_raw = pd.concat(raw_df_lst)
    print(df_raw[["sector",'date']])
    return df_raw
    
    
    
    
def date_preprocess(text):
    '''Grab Date'''
    date = re.search(r'(\d{4}_(january|february|march|april|may|june|july|august|september|october|november|december)_\d{1,2})_', text)
    return date.group(1)

def sector_preprocess(text):  
    '''Grab sector information'''
    sector= re.search(r'.*?--(\D*?)-(project|program|loan|credit){1}', text)
    return sector.group(1)

    
def txt_to_csv(path,out_path):
    '''Input path is path for all text files, output path is path to output
    file'''
    df_raw = txt_to_df(path)
    return df_raw.to_csv(out_path,index=False)


#def main():
#    return

#if __name__ == "__main__":
#    main()

txt_to_df(path)