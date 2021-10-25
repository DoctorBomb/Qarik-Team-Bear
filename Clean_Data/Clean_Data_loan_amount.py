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
# The function first looks for the word "aggregate" in the document and will then look for a loan amounts
# that's in parentheses following this word. If found and in USD, it selects this amount
# (this is to ensure we capture the TOTAL loan if it's broken into smaller pieces)
# If not found after "aggregate", it will check the entire document for the largest number

### Known issues / performance: #####
# Grabs most currency amounts and loan amounts that seem reasonable in size.
# Currently will output about 150 "error" messages when no loan could be found. These entries can be dropped.
# Some outputs don't make much sense, but most do.
# There's no guarantee this will pull the correct amount, but it does do some basic sanity checks
# With different currencies, there's no guarantee that it will pull the correct biggest number

def loan_amount_currency_preprocess(text):
    ''' Grab Loan amount using reg exp'''
    amount=0
    curr='error'
    currency='error'

    # If there's the word "aggregate" in the document, assume it is the best indicator of the total loan amount.
    # Look for a number and letters inside parentheses shortly after the mention of "aggregate".
    # These most likely will be the aggregate loan with currency. If it's not in parentheses, then move on to another
    # possible indicator method.
    if re.search("AGGREGATE",text.upper()): # Determines if the exact word "aggregate" appears in the document
        for txt in re.findall('AGGREGATE [\S\n ]{200}',text.upper()): # Loop through all instances and capture the next 200 chars
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

                # First check if it's USD, if it is, we're likely happy with it if it's large enough
                if ((re.search("US",curr)) or (re.search("\$",curr))):
                    if am > 1000000:
                        amount = am
                        currency = '$'
                        return [amount, currency]
                elif am > amount:
                    amount = am
                    currency = curr

    # Sanity check. Currency should be reasonable in length and amount should be at least 1 million
    if (amount >= 1000000) and (len(currency)<5):

        # Convert all USD / US$ to $'s
        if ((re.search("US",currency)) or (re.search("\$",currency))):
            currency = '$'
        return [amount, currency]

    # Brute force approach, find all numbers in the document in parentheses, find the largest one inside parentheses
    for nums in re.findall("\((.+?\d+?)\)",text):
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
        if am > amount:
            amount = am
            currency = curr

    # Sanity check. Currency should be reasonable in length and amount should be at least 1 million
    if (amount >= 1000000) and (len(currency)<5):
        # Convert all USD / US$ to $'s
        if ((re.search("US",currency)) or (re.search("\$",currency))):
            currency = '$'
        return [amount, currency]
    else:
        return 'Error'

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
