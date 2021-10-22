import re
import pandas as pd
import os
import os.path

##This file is to extract the amortization schedule information using regular expression

MONTH = ("January","February", "March","April", 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')

## main function to extract amortization schedule
##input is a whole text of loan agreement, output is a list consisting of repayment date and amount
def extract_amortization_schedule(text):

    #possible starting index     
    a1 = text.find('Amortization Schedule')
    a2 = text.find('Date Payment Due')
    a3 = text.find('Repayment Schedule')
    starting = [a1,a2,a3]
    search_start_index = new_min(starting)

    
    if search_start_index == -1:
        return ['No keyword']
    else:
        ## determine the search ending index
        ## search no more than 7000 characters. 
        N = 7000
        b1 = text[search_start_index: ].find('Premiums on Prepayment')
        b2 = text[search_start_index: ].find('Premiums Prepayment')
        b3 = text[search_start_index: ].find('prepayment premius')
        b4 = text[search_start_index: ].find('Appendix')
        b5 = text[search_start_index: ].find('APPENDIX')
        b6 = text[search_start_index: ].find('SCHEDULE')
        ending = [b1,b2,b3,b4,b5,b6,N]
        search_end_index = search_start_index + new_min(ending)

        ## only search the part between search_start_index and search_end_index
        search_txt = text[search_start_index:search_end_index]
        #print(search_txt)

        ##If there is "total" keyword, there will be an extra number -- total amount to repay
        ##and we do not need it.
        flags = [search_txt.find('TOTAL'), search_txt.find('Total')]
        flag = max(flags)
    
        ## pattern we are looking for
        date = r'(.*?)(January|February|March|April|May|June|July|August|September|October|November|December)( *[ l\d]{1,2} *),? *(\d\d\d\d)?'
        number = r'(.*?)(\d{1,3} ?([;,]{1} ?[CO\d]{3} ?)?([,;] ?[CO\d]{2,3}){1})\s+'
        percentage =r'.*?(\d+(\.\d+)?%)\s+'
        
        date_result = date_clean(re.findall(date,search_txt))
        # print(date_result, len(date_result))
        number_result = str2num(re.findall(number,search_txt),flag)       
        percentage_result = re.findall(percentage,search_txt)

        #decide which to use numbers or percentages
        amount_result = num_vs_perct(number_result, percentage_result)
        # print(amount_result,len(amount_result))

        #match the date and the amount information
        amtz_schedule = rmbegin(date_result,amount_result)

    return amtz_schedule

############################################################################################################
##This function is used when determining the search range
def new_min(list):
    new_list = []
    for a in list:
        if a != -1:
            new_list.append(a)
    if new_list == []:
        return -1
    else: 
        return min(new_list)

##clean amounts data and change string to numbers, used in function extract_amortization schedule
## Here the flag is indicationg the appearance of "total"
def str2num(amounts,flag):
    new_amounts =[]
    j = 0
    for s in amounts:
        if (flag == -1) or j < len(amounts) - 1:
            j = j + 1
            r1 = re.sub(r'[ ,;]','',s[1])
            r = re.sub(r'[CO]','0',r1)

            ## here we need to manually change to an integer, because the existence of 04
            sum = 0
            i = 0
            d = len(r)
            for char in r:
                sum += int(char)* 10**(d-1-i)
                i += 1

            ## here we only record numbers greater than 2100 to get rid of year numbers
            if sum >= 2100:
                new_amounts.append(sum)      
    return new_amounts


##This function is defined to clean the date, there maybe some extra dates we do not need
def date_clean(dates):

    new_dates = []
    flag = False
    for i in range(len(dates)):
        if re.search(r'Closing',dates[i][0]) or re.search(r'closing',dates[i][0]) or re.search(r'completed by',dates[i][0]):
            flag = False
            continue
        if re.search(r'each',dates[i][0]):
            flag = True
            continue
        if re.search(r'and',dates[i][0]) and flag == True:
            flag = False
            continue
        new_dates.append(dates[i])
    return new_dates

## This function is to decide use numbers or percentages
## For some files, the repayment amount is expressed as the percentage of the total loan amount
def num_vs_perct(numbers, percentages):
    if percentages == []:
        if numbers == []:
            return ["No repayment amount information"]
        elif not('Unrecognized char in numbers' in numbers):
            return numbers
        else:
            return ['Unrecognized char in numbers']
    else:
        return percentages


## this function is to match the repayment date and the amount
## sometimes date information contains begining and ending, try to expand the dates
## based on the assumption that payment is done every half a year
def rmbegin (date, amount):
    new_date_amount= []
    if ('Unrecognized char in numbers' in amount):
        new_date_amount.append(['Unrecognized char in numbers'])
        return new_date_amount
    if ("No repayment amount information" in amount):
        return ["No repayment amount information"]
       
    ##  This number is to record how many "beginning" will appear, ie, the length difference between date and amount
    ## after the beginning appears, then the index for amount and date should differ by the number of beginnings 
    num_begin = 0
    
    d = len(date)
    # Use this flag to record the existence of begining 
    flag = False 

    for i in range(len(date)):
        
        if flag == False:
                ## here we are handling errors, because some times the length of payment date
                ## does not match the length of payment amount
                flag = False
                try:
                    new_date_amount.append([date[i][1]+date[i][2]+ '/'+date[i][3],amount[i- num_begin]])
                except IndexError:
                    new_date_amount.append(['error','error'])
                    break
                else:
                    if re.search(r'(beginning|Beginning|commencing)', date[i][0]):
                        if (len(date) == len(amount)):
                            amount.pop(i)
                        flag = True
                        num_begin += 1
                        m1 = MONTH.index(date[i][1])
                        try:
                            y1 = int(date[i][3])
                        except ValueError:
                            new_date_amount.append(['unrecognized date'])
                            break

                        try:
                            # if date[i+1][0].find('through'):
                                m2 = MONTH.index(date[i+1][1])
                                try:
                                    y2 = int(date[i+1][3])
                                except ValueError:
                                    new_date_amount.append(['unrecognized date'])
                                    break

                                if m1 == m2:
                                    a = 1
                                elif m1 < m2:
                                    a = 2
                                else: 
                                    a = 0

                                # number of pay excluding the start and the end
                                num_pay = (y2 - y1)*2 -2 + a
                                for j in range(num_pay):
                                    new_date_amount.append(['once hallf a year',amount[i  - (num_begin -1)]])
                                    
                                new_date_amount.append([date[i+1][1]+date[i+1][2]+ '/'+date[i+1][3],amount[i  - (num_begin -1)]])
                            
                        except IndexError:
                            new_date_amount.append(['error','error'])
        else:
            flag = False
    if d - len(amount) != num_begin:
        new_date_amount.append(["number not match"])        
    return new_date_amount


##################################################################################################################################################################
## define the extration function for all files 
## input is the path to the folder, output is a dictionary
error_message = (['error','error'],['number not match'], ['No keyword'], ['Unrecognized char in numbers'],['unrecognized date'])
def extract_amortization_schedule_files(path):
    dic = {}
    files = listdir_nohidden(path)
    num_files = 0
    for file_name in files:
        num_files += 1
        if (num_files >-1)  :
            file_path = os.path.join(path, file_name)
            #print(type(file_name))
            f = open(file_path,'r')
            txt = f.read()
            r = extract_amortization_schedule(txt)
            flag = 'Success'
        
            if any (m in r for m in error_message):
                flag = 'Fail'
            dic[file_name] = [r, flag]
            f.close()
    print('There are %d files in total' %(num_files))
    return dic

############################################################################################################
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
            #print(key)
            #print(dic[key][0])
        # else:
        #     print(dic[key][0])
    return count 

############################################################################################################

##Check the performance on all files
path1 = '/Users/bingjinliu/Desktop/Erdos Institute/project/github/FinanceErdosProj/Tesseract_Text'
path2 = '/Users/bingjinliu/Desktop/Erdos Institute/project/github/FinanceErdosProj/PyMuPdf_Text'
dic =  extract_amortization_schedule_files(path2)
print(count_errors(dic))