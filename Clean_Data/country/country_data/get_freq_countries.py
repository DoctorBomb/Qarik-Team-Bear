import os
import numpy as np
import pandas as pd
import copy

path = "/Users/attiliocastano/Documents/GitHub/FinanceErdosProj/country_data/"

DF_tess = pd.read_csv(os.path.join(path,'tess_only_countries.csv'))
DF_pdf = pd.read_csv(os.path.join(path,'PyMU_only_countries.csv'))
countries = pd.read_csv(os.path.join(path,'countries.csv'))

country_list = countries.Country.values.tolist()
countries_low = [x.lower().strip() for x in country_list]

import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_md")

matcher_countries = Matcher(nlp.vocab)

for c in countries_low:
    pattern = [{'LOWER': {'REGEX': x}} for x in c.split()]
    matcher_countries.add(c, [pattern])


def count_no_countries(data):
    count = len(data)
    for file in data.countries:
        doc = nlp.make_doc(file)
        matches = matcher_countries(doc)
        for match_id, start, end in matches:
            count = count-1
            break
    return count

'''
print(count_no_countries(DF_tess))
Returns: 4

print(count_no_countries(DF_pdf))
Returns: 1
'''


matcher_nums = Matcher(nlp.vocab)
matcher_nums.add('number', [[{'IS_DIGIT' : True}]])


def countries_string_to_list(data_instance):
    '''
    data_instace a file (i.e. row) in DF_tess or DF_pdf.
    returns list of countries and frequency as a list, as opposed to a string

    recall that pandas data frame can only record objects of a single type.
    And we already have the name of the file which is a string
    '''

    doc = nlp(data_instance.countries)
    matches_countries = matcher_countries(doc)
    matches_nums = matcher_nums(doc)
    country_names = []
    country_times = []
    for match_id, start, end in matches_countries:
        string_id = nlp.vocab.strings[match_id]
        if not(string_id in country_names):
            country_names.append(string_id)
    for match_id, start, end in matches_nums:
        country_times.append(int(doc[start:end].text))

    #return_for_index = list([country_names, country_times])
    #data_copy = copy.deepcopy(data)
    #data_copy.at[i, 'countries'] = return_for_index
    return [country_names, country_times]



def total_frequency_of_countries(data):
    '''
    data is in DF_tess or in DF_pdf
    outputs dic with the frecuency that each country has been mentioned among
    all documents

    returns dictionary with country -> number of loans in which it appears
    '''

    dic = {x:0 for x in countries_low}
    for i in data.index:
        raw_list = countries_string_to_list(data.loc[i])
        countries_in_list = raw_list[0]
        frequency_in_list = raw_list[1]
        for country in countries_in_list:
            dic[country] = dic[country] + 1
    return dic




'''
T = frequency_of_countries(DF_tess)
print(T['united states'])
#Return 343 out of 354 files

P = frequency_of_countries(DF_pdf)
print(P['united states'])
#Returns 2778 out of 2806 files
'''

tess_total_countries_dic = total_frequency_of_countries(DF_tess)
pdf_total_countries_dic = total_frequency_of_countries(DF_pdf)

total_dic = {x: tess_total_countries_dic[x] + pdf_total_countries_dic[x] for x in countries_low}


'''
Finally, we create a dataframe which is sorted by the frequency of how often
countries are mentioned in the loans
'''

sorted_countries_tuples = sorted(total_dic.items(), key = lambda item: item[1], reverse = True)
sorted_countries_dic = {k: v for k, v in sorted_countries_tuples}

sorted_countries_df = pd.DataFrame.from_dict(sorted_countries_dic, orient='index', columns = ['num_doc_mentioned'])
#print(sorted_countries_df)
#print(sorted_countries_df.head())

#sorted_countries_df.to_csv('freq_countries_mentioned.csv', index = True)
