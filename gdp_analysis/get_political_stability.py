import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_md')

gdp_df = pd.read_csv('gdp_analysis.csv')
#gdp_df.drop(columns = 'political_stability', inplace = True)
gdp_df.insert(loc = 6, column = 'political_stability', value = np.zeros(len(gdp_df.index)))

stability_df = pd.read_csv('wgidataset.csv')

country_list = gdp_df.country_name.values.tolist()
matcher_country = Matcher(nlp.vocab)
for country_name in country_list:
    pattern = [{'LOWER': {'REGEX': x}} for x in country_name.split()]
    matcher_country.add(country_name, [pattern])



stability_years = stability_df.columns[1:,].tolist()
for index in stability_df.index:
    mean_st_index = np.round(np.mean(stability_df.loc[index, stability_years].values), 3)
    doc = nlp(stability_df.loc[index, 'Country'])
    matches = matcher_country(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        match_gdp_index = gdp_df[gdp_df.loc[:, 'country_name'] == string_id].index
        for x in match_gdp_index:
            gdp_df.at[x, 'political_stability'] = mean_st_index


#gdp_df.to_csv('gdp_analysis.csv', index = False)
