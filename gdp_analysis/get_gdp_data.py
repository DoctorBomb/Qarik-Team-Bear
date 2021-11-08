import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import spacy
from spacy.matcher import Matcher

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

nlp = spacy.load('en_core_web_md')

gdp_df = pd.read_csv('gdp.csv', header = 2)
gdp_df.drop(columns = 'Unnamed: 65', inplace = True)
#print(gdp_df.shape) # = (266, 65)

countries = pd.read_csv('countries.csv')
#print(countries.shape) # = (227,20)
country_list = countries.Country.values.tolist()
countries_low = [x.lower().strip() for x in country_list]
#countries_low.append('None')



def get_match_country(country_name):
    '''
    Takes as input the country name, lower case (as recognized by the matcher).
    Outputs the line of the data frame where this country is in the gdp_df Data Frame.
    '''
    matcher_country = Matcher(nlp.vocab)
    pattern = [{'LOWER': x} for x in country_name.split()]
    #189 No Regex
    #198 With Regex
    matcher_country.add(country_name, [pattern])
    for index in gdp_df.index:
        doc = nlp(gdp_df.loc[index, 'Country Name'])
        match = matcher_country(doc)
        if len(match)> 0:
            for match_id, start, end in match:
                country_in_gdp_df = doc[start:end].text
            return gdp_df[gdp_df.loc[:, 'Country Name'] == country_in_gdp_df]
        else:
            pass
    return pd.DataFrame()



def get_linear_reg(gdp_per_country, country_name):
    '''
    Takes as input a data frame with a single entry, and outputs a new single instanced
    data frame containing the information of the linear regression
    '''
    if gdp_per_country.empty:
        return pd.DataFrame()
    else:
        years = np.linspace(1960, 2020, num = 61, dtype = int)
        for index in gdp_per_country.index:
            X_year = np.array([])
            y_gdp = np.array([])
            #country_name = str(gdp_per_countr.loc[index, 'Country Name']).lower().strip()
            for year in years:
                if str(gdp_per_country.loc[index, str(year)]) == 'nan':
                    pass
                else:
                    X_year = np.append(X_year, year)
                    y_gdp = np.append(y_gdp, gdp_per_country.loc[index, str(year)])

            if len(X_year)>0:

                LR = LinearRegression()
                LR.fit(X_year.reshape(-1,1), y_gdp)
                slope = LR.coef_
                intercept = LR.intercept_
                min_year = np.amin(X_year)
                max_year = np.amax(X_year)

                gdp_scaler = StandardScaler()
                gdp_scaler.fit(LR.predict(X_year.reshape(-1,1)).reshape(-1,1))
                volatility = mean_squared_error(gdp_scaler.transform(y_gdp.reshape(-1,1)),
                gdp_scaler.transform(LR.predict(X_year.reshape(-1,1)).reshape(-1,1)), squared = False)

                data_d = {'country_name': country_name, 'slope' : slope,
                'y_intercept' : intercept, 'volatility' : volatility,
                'min_year' : min_year, 'max_year' : max_year}
                return pd.DataFrame(index = [index], data = data_d)
            else:
                return pd.DataFrame()


def get_gdp_data_frame():
    data_frame = pd.DataFrame(columns = ['country_name', 'slope', 'y_intercept',
    'volatility', 'min_year', 'max_year'])
    for country in countries_low:
        D = get_linear_reg(get_match_country(country), country)
        data_frame = data_frame.append(D)
    return data_frame

#get_gdp_data_frame().to_csv('gdp_analysis.csv', index = False)
#print(get_gdp_data_frame())
