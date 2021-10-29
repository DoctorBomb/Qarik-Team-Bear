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
countries_low.append('None')

country_region_dic = {'None': 'None'}
for i in countries.index:
    country = countries.loc[i, 'Country']
    region = countries.loc[i, 'Region']
    country_region_dic[country.lower().strip()] = region.lower().strip()


import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_md")

matcher_countries = Matcher(nlp.vocab)

for c in countries_low:
    pattern = [{'LOWER': {'REGEX': x}} for x in c.split()]
    matcher_countries.add(c, [pattern])


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


def get_max_country(list_freq):
    '''
    Takes as input a list of dim 2, where each row contains a country and the
    number of times it has been mentioned in a loan documents
    Outputs a single country name which is the country that is mentioned the most.
    If two countries were mentioned the same number of times, we return the
    one that was mentioned the most

    '''
    #list_to_df = pd.DataFrame(list_freq[0], list_freq[1])
    if len(list_freq[1]) > 0:
        index = np.argmax(np.array(list_freq[1]))
        #print(list_freq[0][index])
        country = list_freq[0][index]
    else:
        country = 'None'
    return country


def max_frequency_of_countries(data):
    '''
    data is in DF_tess or in DF_pdf
    outputs dic with the frecuency that each country has been mentioned among
    all documents

    returns dictionary with country -> number of loans were country has max appearance
    '''

    dic = {x:0 for x in countries_low}
    for i in data.index:
        raw_list = countries_string_to_list(data.loc[i])
        country = get_max_country(raw_list)
        dic[country] = dic[country] + 1
    return dic


def insert_max_country(data):
    for i in data.index:
        data.at[i, 'max_country'] = get_max_country(countries_string_to_list(data.iloc[i]))
        data.at[i, 'world_region'] = country_region_dic[data.loc[i, 'max_country']]
    return data


'''
Modify the data frames to include a new row where we will record the countries that where mentioned the most
'''
DF_tess.insert(loc = 2, column = 'max_country', value  = [ 'Blank' for x in DF_tess.index])
DF_pdf.insert(loc = 2, column = 'max_country', value  = [ 'Blank' for x in DF_pdf.index])

DF_tess.insert(loc = 3, column = 'world_region', value  = [ 'Blank' for x in DF_tess.index])
DF_pdf.insert(loc = 3, column = 'world_region', value  = [ 'Blank' for x in DF_pdf.index])

insert_max_country(DF_tess)
insert_max_country(DF_pdf)


#DF_tess.to_csv('tess_max_countries.csv', index = False)
#DF_pdf.to_csv('PyMU_max_countries.csv', index = False)

'''

tess_max_countries_dic = max_frequency_of_countries(DF_tess)
pdf_max_countries_dic = max_frequency_of_countries(DF_pdf)

max_dic = {x: tess_max_countries_dic[x] + pdf_max_countries_dic[x] for x in countries_low}

sorted_max_countries_tuples = sorted(max_dic.items(), key = lambda item: item[1], reverse = True)
sorted_max_countries_dic = {k: v for k, v in sorted_max_countries_tuples}

sorted_max_countries_df = pd.DataFrame.from_dict(sorted_max_countries_dic, orient='index', columns = ['num_doc_max'])

'''

#print(sorted_max_countries_df)
#print(sorted_max_countries_df.head())

#sorted_max_countries_df.to_csv('max_countries_mentioned.csv', index = True)
