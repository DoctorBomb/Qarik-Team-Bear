#! /usr/bin/env python3

from itertools import *
import numpy as np
import pandas as pd

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
