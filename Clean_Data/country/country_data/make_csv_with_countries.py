import os
import numpy as np
import pandas as pd

path = "/Users/attiliocastano/Documents/GitHub/FinanceErdosProj/country_data/"

DF_tess_txt = pd.read_csv(os.path.join(path,'Tesseract_DF_with_countries.csv'))
DF_pdf_txt = pd.read_csv(os.path.join(path,'PyMuPdf_DF_with_countries.csv'))

def drop_raw_txt(data):
    return data.drop(columns= 'raw_txt')

DF_tess_no_txt = drop_raw_txt(DF_tess_txt)
DF_pdf_no_txt = drop_raw_txt(DF_pdf_txt)

#print(DF_tess_no_txt)
#print(DF_pdf_no_txt)

#DF_tess_no_txt.to_csv('tess_only_countries.csv', index = False)
#DF_pdf_no_txt.to_csv('PyMU_only_countries.csv', index = False)
