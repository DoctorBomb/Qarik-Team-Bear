import re
import pandas as pd
import os
import os.path


## define the function to extract the sector information and the date of loan agreement from the name of files
## file_name is a string, the function returns the list of strings describing sector and date
def extract_sector_date(file_name):
    sector= re.search(r'.*?--(\D*?)-(project|program|loan|credit){1}', file_name)
    date = re.search(r'(\d{4}_(january|february|march|april|may|june|july|august|september|october|november|december)_\d{1,2})_', file_name)
    sector_date =[]
    if sector:
            sector_date.append(sector.group(1))
    else:
            sector_date.append('error')
    if date:
            sector_date.append(date.group(1))
    else:
            sector_date.append('error')
    return sector_date

## This function is to extract the sector and date information for all files in a path
## Input is the name of the path, it is a string, 
## output is a dictionary with keys being filename and values being the list of sector and date
def extract_sector_date_files(path):
    dic = {}
    files = listdir_nohidden(path)
    for file_name in files:       
        r = extract_sector_date(file_name)
        flag = 'Success'
    
        if ('error' in r[1]):
            flag = 'Fail'
        dic[file_name] = [r, flag]
    return dic

## The listdir may return some unwanted hidden file. This function is to ignore those files
def listdir_nohidden(path):
    files = os.listdir(path)
    files.sort()
    for f in files:
        if not f.startswith('.'):
            yield f


## This function is to display the performance of extraction function 
def count_errors(dic):
    count = 0
    for key in dic.keys():
        if dic[key][1] == 'Fail':
            count +=1
            print(key)
            #print(dic[key][0])
        # else:
        #     print(dic[key][0])
    return count 



##Check the performance on all files
path1 = '/Users/bingjinliu/Desktop/Erdos Institute/project/github/FinanceErdosProj/Tesseract_Text'
path2 = '/Users/bingjinliu/Desktop/Erdos Institute/project/github/FinanceErdosProj/PyMuPdf_Text'
dic = extract_sector_date_files(path2)
print(count_errors(dic))