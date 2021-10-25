import os
import numpy as np
import pandas as pd

path = "/Users/attiliocastano/Documents/GitHub/FinanceErdosProj/country_data/"

DF_tess = pd.read_csv(os.path.join(path,'tess_only_countries.csv'))
DF_pdf = pd.read_csv(os.path.join(path,'PyMU_only_countries.csv'))


import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_md")

countries = pd.read_csv(os.path.join(path,'countries.csv'))

for index in DF_pdf.sample(20).index:
    print(DF_pdf.loc[index, 'countries'])
