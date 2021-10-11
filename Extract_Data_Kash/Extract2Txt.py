#! /usr/bin/env python3

import pytesseract
from pdf2image import convert_from_path 
import os
#import subprocess
import pandas as pd

## Set path where pdf files are
path = "/home/kbari/Documents/Erdos/pdfminer_texts/"

## PDF Miner pass
def pdfminer_pass():
    ''' PDF Miner.Six first pass; Calls bash script; requires it be executable (chmod +x pdfmine.sh)'''
    os.system('./pdfmine.sh')
    #subprocess.call(['sh',path+'pdfmine.sh'])
    return

## INC
def check(thresh):
    ''' Determine which files are did not get extracted with pdfminer; Checks
    file size'''
    return 

## Tesseract OCR pass; INC
def tesseract_pass(list_of_img_pdfs):
    ''' Runs Tesseract OCR on list of pdfs '''
    #tesseract_parse = []
    for file in list_of_img_pdfs:
        out = convert_from_path(file,500)
        text = ''    
        for o in out:
            text += str(pytesseract.image_to_string(o))
        file1 = open(os.path.splitext(os.path.basename(f))[0]+".txt","w")
        file1.writelines(text)
        file1.close()
    #df_tesser = pd.DataFrame(tesseract_parse,columns=[list_of_img_pdfs])
    return


##Convert from txt files to a dataframe; Other information to include possibly?
def txt_to_df(path):
    DIR = os.listdir(path)
    raw_df_lst = []
    #pd.read_table(file,header=None,quotechar=None,quoting=3,error_bad_lines=False) for file in DIR]
    for i in range(len(DIR)):
        with open(DIR[i]) as f:
            lines = f.readlines()
            data = '\n'.join(map(str,lines))
            di = pd.DataFrame([data,len(lines),len(data)],index=['raw_text','num_lines','num_char'],columns=[DIR[i]]).T
            raw_df_lst.append(di)
    #print(len(raw_df_lst))
    df_raw = pd.concat(raw_df_lst)
    return df_raw


