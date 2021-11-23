import os
import numpy as np
import pandas as pd


path_to_pdf = "/Users/attiliocastano/Documents/GitHub/Raw_Data/PyMuPdf_Text/"
path_to_tess = "/Users/attiliocastano/Documents/GitHub/Raw_Data/Tesseract_Text/"

def txt_to_df(path):
    ''' Put all txt files into single dataframe'''
    DIR = os.listdir(path)
    raw_df_lst = []
    for i in range(len(DIR)):
        with open(path+DIR[i],encoding = "ISO-8859-1") as f:
            lines = f.readlines()
            data = '\n'.join(map(str,lines))
            di = pd.DataFrame(data = {'proj_name': [DIR[i]], 'raw_txt': [data]})
            raw_df_lst.append(di)
    #print(len(raw_df_lst))
    df_raw = pd.concat(raw_df_lst)
    return df_raw


DF_pdf = txt_to_df(path_to_pdf)
DF_tess = txt_to_df(path_to_tess)


#DF_pdf.to_csv('PyMuPdf_DF', index = False)
#DF_tess.to_csv('Tesseract_DF', index = False)
