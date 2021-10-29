#! /usr/bin/env python3

from itertools import *
import os
import numpy as np
import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
#nltk.download()

# Will grab the loan amount and currency of a text file. If you want to apply this to a dataframe, use:
# raw_df['loan_amount_curr'] = raw_df.raw_text.apply(lambda x: loan_amount_currency_preprocess(x))

##### Returns as a list! #####
# Another file, create_df_from_list, will help split the list into two new columns
# raw_df = create_df_from_list(raw_df, 'loan_amount_curr')
# raw_df = raw_df.rename(columns={'loan_amount_curr_0': 'loan_amount', 'loan_amount_curr_1': 'currency'})

##### Idea of function: #####
# The function first looks for 'article' twice and then the word 'the loan' hoping to capture
# a trend seen in the documents. It prefers between Article II and III to capture the loan amount
# if not found, it will search for the word "aggregate" in the document and will then look for a loan amounts
# that's in parentheses following this word. If found and in USD, it selects this amount
# (this is to ensure we capture the TOTAL loan if it's broken into smaller pieces)
# If not found after "aggregate", it will check the entire document for the largest number

### Known issues / performance: #####
# Grabs most currency amounts and loan amounts that seem reasonable in size.
# Currently will output about 150 "error" messages when no loan could be found. These entries can be dropped.
# There's no guarantee this will pull the correct amount, but it does do some basic sanity checks
# With different currencies, there's no guarantee that it will pull the correct biggest number

def loan_amount_currency_preprocess(text):
    ''' Grab Loan amount using reg exp'''
    amount=0
    curr='error'
    currency='error'

    # First try to look between Articles II and III for the loan amount...
    # Will try to capture the biggest number in Article II in hopes that is correct
    if (re.search('ARTICLE II ',text.upper()) or re.search('ARTICLE II\n',text.upper())):
        spacer1 = 'ARTICLE II'
    elif (re.search('ARTICLE 11 ',text.upper()) or re.search('ARTICLE 11\n',text.upper())):
        spacer1 = 'ARTICLE 11'
    elif (re.search('ARTICLE 2 ',text.upper()) or re.search('ARTICLE 2\n',text.upper())):
        spacer1 = 'ARTICLE 2'

    if (re.search('ARTICLE III ',text.upper()) or re.search('ARTICLE III\n',text.upper())):
        spacer2 = 'ARTICLE III'
    elif (re.search('ARTICLE 111 ',text.upper()) or re.search('ARTICLE 111\n',text.upper())):
        spacer2 = 'ARTICLE 111'
    elif (re.search('ARTICLE 3 ',text.upper()) or re.search('ARTICLE 3\n',text.upper())):
        spacer2 = 'ARTICLE 3'

    try:
        reg_ex = spacer1 + '[\S\n ]*?' + '(THE LOAN[\S\n ]*?' + spacer2 + ')'
    except:
        # Try to be less specific. Hope the first capture will work
        # First looks for two Articles, hoping to catch the 2nd article and then 'the loan' after it
        reg_ex = 'ARTICLE[\S\n ]*?ARTICLE[\S\n ]*?(THE LOAN[\S\n ]+?\(.+?\d+?\))'

    if re.search(reg_ex,text.upper()):
        for txt in re.findall('[\S\n ]{50}\(.+?\d+?\)',re.findall(reg_ex,text.upper())[0]): # Loop through all instances
            for nums in re.findall("\((.+?\d+?)\)",txt):
                am = nums.replace(',','')
                am = am.replace('?','')
                am = am.replace(' ','')
                try:
                    curr = re.findall("\D+",am)[0]
                except:
                    # Most likely means there is no currency present
                    continue
                am = re.findall("\d+",am)[0]
                am = int(am)

                # Convert currencies
                curr = currency_corr(curr)

                # The document may fail to load the proper currency, try to grab the currency from the name beforehand
                if ((curr != "$") and (curr != "EUR") and (curr != "SDR") and (curr != "GBP") and (curr != "FRF")
                    and (curr != "JPY") and (curr != "DEM") and (curr != "INR") and (curr != "RM") and (curr != "SEK")):
                    try:
                        curr = re.findall('MILLION([\S\n ]+\()',txt.upper())[0]
                        curr = re.findall('\w+(?=\s+\()',curr)[0]
                        curr = currency_corr(curr)
                    except:
                        pass
                    try:
                        curr = re.findall('BILLION([\S\n ]+\()',txt.upper())[0]
                        curr = re.findall('\w+(?=\s+\()',curr)[0]
                        curr = currency_corr(curr)
                    except:
                        pass

                if am > amount:
                    amount = am
                    currency = curr

    # Likely preferable to a brute-force approach, so settle on this loan amount if reasonable
    # Sanity check. Currency should be reasonable in length and amount should be at least 1 million
    if (amount >= 1000000) and (len(currency)<5):
        # Correct all currencies to proper forms
        currency = currency_corr(currency)

        # At this point, the currency probably isn't worth remembering
        if ((currency == "$") or (currency == "EUR") or (currency == "SDR") or (currency == "GBP")
            or (currency == "FRF") or (currency == "JPY") or (currency == "DEM") or (currency == "INR")
            or (currency == "RM") or (currency == "SEK")):
            return [amount, currency]

    # This could possibly fail as other aspects of the document may mention "aggregate". ¯\_(ツ)_/¯
    # Prefer finding the word 'aggregate' for the loan amount
    if re.search("AGGREGATE",text.upper()): # Determines if the exact word "aggregate" appears in the document
        for txt in re.findall('AGGREGATE [\S\n ]{150}',text.upper()): # Loop through all instances and capture the next 200 chars
            for nums in re.findall("\((.+?\d+?)\)",txt): # Find all numbers with other characters inside of parentheses
                am = nums.replace(',','')
                am = am.replace('?','')
                am = am.replace(' ','')
                try:
                    curr = re.findall("\D+",am)[0]
                except:
                    # Most likely means there is no currency present
                    continue
                am = re.findall("\d+",am)[0]
                am = int(am)

                # Convert currencies
                curr = currency_corr(curr)

                # The document may fail to load the proper currency, try to grab the currency from the name beforehand
                if ((curr != "$") and (curr != "EUR") and (curr != "SDR") and (curr != "GBP") and (curr != "FRF")
                    and (curr != "JPY") and (curr != "DEM") and (curr != "INR") and (curr != "RM") and (curr != "SEK")):
                    try:
                        curr = re.findall('MILLION([\S\n ]+\()',txt.upper())[0]
                        curr = re.findall('\w+(?=\s+\()',curr)[0]
                        curr = currency_corr(curr)
                    except:
                        pass
                    try:
                        curr = re.findall('BILLION([\S\n ]+\()',txt.upper())[0]
                        curr = re.findall('\w+(?=\s+\()',curr)[0]
                        curr = currency_corr(curr)
                    except:
                        pass

                # First check if it's USD, if it is, we're likely happy with it if it's large enough
                if ((curr=='$') and (am > 1000000)):
                    return [am, curr]
                elif am > amount:
                    amount = am
                    currency = curr

    # Sanity check. Currency should be reasonable in length and amount should be at least 1 million
    if (amount >= 1000000) and (len(currency)<5):

        # Correct all currencies to proper forms
        currency = currency_corr(currency)

        # At this point, the currency probably isn't worth remembering
        if ((currency == "$") or (currency == "EUR") or (currency == "SDR") or (currency == "GBP")
            or (currency == "FRF") or (currency == "JPY") or (currency == "DEM") or (currency == "INR")
            or (currency == "RM") or (currency == "SEK")):
            return [amount, currency]

    # Brute force approach, find all numbers in the document in parentheses, find the largest one inside parentheses
    for txt in re.findall('[\S\n ]{100}\(.+?\d+?\)',text): # Loop through all instances and capture the next 200
        for nums in re.findall("\((.+?\d+?)\)",txt):
            am = nums.replace(',','')
            am = am.replace('?','')
            am = am.replace(' ','')
            try:
                curr = re.findall("\D+",am)[0]
            except:
                # Most likely means there is no currency present
                continue
            am = re.findall("\d+",am)[0]
            am = int(am)

            # Convert currencies
            curr = currency_corr(curr)

            # The document may fail to load the proper currency, try to grab the currency from the name beforehand
            if ((curr != "$") and (curr != "EUR") and (curr != "SDR") and (curr != "GBP") and (curr != "FRF")
                and (curr != "JPY") and (curr != "DEM") and (curr != "INR") and (curr != "RM") and (curr != "SEK")):
                try:
                    curr = re.findall('MILLION([\S\n ]+\()',txt.upper())[0]
                    curr = re.findall('\w+(?=\s+\()',curr)[0]
                    curr = currency_corr(curr)
                except:
                    pass
                try:
                    curr = re.findall('BILLION([\S\n ]+\()',txt.upper())[0]
                    curr = re.findall('\w+(?=\s+\()',curr)[0]
                    curr = currency_corr(curr)
                except:
                    pass

            if am > amount:
                amount = am
                currency = curr

    # Sanity check. Currency should be reasonable in length and amount should be at least 1 million
    if (amount >= 1000000) and (len(currency)<5):
        # Correct all currencies to proper forms
        currency = currency_corr(currency)
        # At this point, the currency probably isn't worth remembering
        if ((currency != "$") and (currency != "EUR") and (currency != "SDR") and (currency != "GBP")
            and (currency != "FRF") and (currency != "JPY") and (currency != "DEM") and (currency != "INR")
            and (currency != "RM") and (currency != "SEK")):
            return 'Error'
        else:
            return [amount, currency]
    else:
        return 'Error'

# Will convert currencies to a standard form
def currency_corr(text):
    if ((re.search("US",text.upper())) or (re.search("\$",text)) or (re.search("dollar",text.lower()))):
        return '$' #US Dollar
    elif ((re.search("EUR",text.upper())) or (re.search("\€",text)) or (text.upper()=='E')):
        return 'EUR' #Euro
    elif (re.search("SDR",text.upper()) or (re.search("right",text.lower()))):
        return 'SDR' #Special Drawing Rights
    elif ((re.search("POUND",text.upper())) or (re.search("\£",text)) or (re.search("GBP",text.upper()))):
        return 'GBP' #British Pound
    elif (re.search("FRF",text.upper()) or (re.search("frank",text.lower()))):
        return 'FRF' #Franks
    elif ((re.search("JPY",text.upper())) or (re.search("\¥",text)) or (re.search("yen",text.lower()))):
        return 'JPY' #Japanese Yen
    elif ((re.search("DEM",text.upper())) or (re.search("DM",text.upper())) or (re.search("mark",text.lower()))):
        return 'DEM' #Deutsche Mark
    elif (re.search("INR",text.upper()) or (re.search("rupee",text.lower()))):
        return 'INR' #Indian Rupee
    elif (re.search("RM",text.upper()) or (re.search("ringgit",text.lower()))):
        return 'RM' #Malaysian Ringgit
    elif (re.search("SEK",text.upper()) or (re.search("krona",text.lower()))):
        return 'SEK' #Swedish Krona
    else:
        # No currency found, return what was input
        return text

# def loan_amount_preprocess1(text):
#     ''' Grab Loan amount using reg exp'''
#     start = 'ARTICLE II'
#     end =  'ARTICLE III'
#     try:
#         t1 = (text.split(start)[1].split(end)[0])
#         r = re.search("\((.+?)\)",t1).group(1)
#         #print('r=',r)
#         if contains_number(r):
#             return r
#     except:
#         pass
#     try:
#         t1 = (text.split(start)[1].split(end)[0])
#         r = re.findall("\$.+?\s",t1)[0]
#         if contains_number(r):
#             return r
#     except:
#         pass
#     start = 'ARTICLE H'
#     end =  'ARTICLE III'
#     try:
#         t1 = (text.split(start)[1].split(end)[0])
#         r1 = re.search("\((.+?)\)",t1).group(1)
#         #print('r1=',r1)
#         if contains_number(r1):
#             return r1
#     except:
#         pass
#     start = 'ARTICLE H'
#     end =  'ARTICLE M'
#     try:
#         t1 = (text.split(start)[1].split(end)[0])
#         r2 = re.search("\((.+?)\)",t1).group(1)
#         #print('r2=',r2)
#         if contains_number(r2):
#             return r2
#     except:
#         pass
#     start = 'ARTICLE II'
#     end =  'ARTICLE M'
#     try:
#         t1 = (text.split(start)[1].split(end)[0])
#         r3 = re.search("\((.+?)\)",t1).group(1)
#         #print('r3=',r3)
#         if contains_number(r3):
#             return r3
#     except:
#         pass
#
# def contains_number(reg_exp):
#     y = [char.isdigit() for char in reg_exp]
#     if y.count(True) > 5:
#         return True
#     return False

# def loan_amount_preprocess0(text):
#     ''' Grab Loan amount '''
#     start = 'ARTICLE II'
#     end =  'ARTICLE III'
#     t1 = (text.split(start)[1].split(end)[0])
#     t = [s.translate(str.maketrans('','',string.punctuation)) for s in t1.split()]
#     n = [int(i) for i in t if i.isdigit()]
#     n = [i for i in n if i%100000 == 0]
#     return max(n)

#def main():
#    return

#if __name__ == "__main__":
#    main()
