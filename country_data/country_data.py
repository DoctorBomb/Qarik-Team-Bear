import os
import numpy as np
import pandas as pd

path = "/Users/attiliocastano/Documents/GitHub/FinanceErdosProj/country_data/"

pdf_DF = pd.read_csv(os.path.join(path,'PyMuPdf_DF.csv'))
tess_DF = pd.read_csv(os.path.join(path,'Tesseract_DF.csv'))
countries = pd.read_csv(os.path.join(path,'countries.csv'))

pdf_DF.insert(loc = 1, column = 'countries', value  = [ [] for x in pdf_DF.index])
tess_DF.insert(loc = 1, column = 'countries', value  = [ [] for x in tess_DF.index])

country_list = countries.Country.values.tolist()
countries_low = [x.lower().strip() for x in country_list]



import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_md")

matcher = Matcher(nlp.vocab)

for c in countries_low:
    pattern = [{'LOWER': {'REGEX': x}} for x in c.split()]
    matcher.add(c, [pattern])

def insert_list_countries(data):
    for i in data.index:
        print(i)
        doc = nlp.make_doc(data.loc[i , 'raw_txt'])
        matches = matcher(doc)
        relevant_countries = []
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            relevant_countries.append(string_id)
        relevant_countries_list, relevant_countries_values = np.unique(np.array(relevant_countries), return_counts = True)
        data.at[i , 'countries'] = [relevant_countries_list.tolist(), relevant_countries_values.tolist()]
        #print(data.loc[i , 'countries'])

#insert_list_countries(tess_DF)
#tess_DF.to_csv('Tesseract_DF_with_countries', index = False)

#insert_list_countries(pdf_DF)
#pdf_DF.to_csv('PyMuPdf_DF_with_countries.csv', index = False)
