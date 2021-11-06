import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


gdp_df = pd.read_csv('gdp_analysis.csv')
loan_countries = pd.read_csv('max_countries_mentioned.csv')
loan_countries.rename(columns = {'Unnamed: 0': 'country_name'}, inplace = True)

mentioned_countries = pd.read_csv('freq_countries_mentioned.csv')
mentioned_countries.rename(columns = {'Unnamed: 0': 'country_name'}, inplace = True)

gdp_df.insert(loc = len(gdp_df.columns), column = 'got_loan', value = np.zeros(len(gdp_df.index)))
gdp_df.insert(loc = len(gdp_df.columns), column = 'got_mentioned', value = np.zeros(len(gdp_df.index)))

for index_country in loan_countries.index:
    if loan_countries.loc[index_country, 'num_doc_max'] == 0:
        pass
    else:
        country = loan_countries.loc[index_country, 'country_name']
        for index_gdp in gdp_df.index:
            if country == gdp_df.loc[index_gdp, 'country_name']:
                gdp_df.at[index_gdp, 'got_loan'] = float(1)

for index_mentioned in mentioned_countries.index:
    if mentioned_countries.loc[index_mentioned, 'num_doc_mentioned'] == 0:
        pass
    else:
        country = mentioned_countries.loc[index_mentioned, 'country_name']
        for index_gdp in gdp_df.index:
            if country == gdp_df.loc[index_gdp, 'country_name']:
                gdp_df.at[index_gdp, 'got_mentioned']= float(1)

#gdp_df.to_csv('gdp_analysis.csv', index = False)
