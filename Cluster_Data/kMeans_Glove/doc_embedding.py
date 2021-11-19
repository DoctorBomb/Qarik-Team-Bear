import pandas as pd
import numpy as np
import pandas as pd
import re
from itertools import chain
from collections import defaultdict
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import linecache



nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('words')
words = set(nltk.corpus.words.words())


alphabet_string = string.ascii_lowercase
other = ['project','program','borrower','may','can','objective','sector']
month = [ "january","february", "march","april", 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
deleted_word = list(chain(alphabet_string, other, month, stopwords.words('english')))
stemmer = WordNetLemmatizer()

sec= ['agricultural', 'extension', 'research', 'support', 'activity', 'crop', 'fishery', 'forestry', 'irrigation',
 'drainage', 'livestock', 'agriculture', 'fishing', 'public', 'administration', 'adult', 'basic', 'continue', 'education', 
 'early', 'childhood', 'primary', 'secondary', 'tertiary', 'workforce', 'development', 'skill', 'energy', 'transmission', 
 'distribution', 'mining', 'non', 'renewable', 'generation', 'oil', 'gas', 'extractives', 'biomass', 'geothermal', 'hydro', 
 'solar', 'wind', 'banking', 'institution', 'capital', 'market', 'insurance', 'pension', 'bank', 'financial', 'health', 'facility',
  'construction', 'commercialization', 'agri', 'business', 'housing', 'manufacturing', 'industry', 'trade', 'service', 'tourism', 'ict',
   'infrastructure', 'information', 'communication', 'technology', 'central', 'government', 'agency', 'law', 'justice', 'sub', 'national', 
   'social', 'protection', 'aviation', 'transportation', 'port', 'waterway', 'railway', 'rural', 'inter', 'urban', 'road', 'transport', 'water', 
   'supply', 'sanitation', 'waste', 'management', 'engergy', 'finance']

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def new_text_preprocess(text):
    '''
    Remove all punctuation,stopwords, lemmatize -> returns list of words
    '''
    word_list =[]
    nopunc = re.sub(r'[^a-zA-Z]',' ',text)
    nopunc = [w.lower() for w in nopunc.split()]
    for word in nopunc:
        if word != 'and' and str.find('and', word) == 0:
                word = word[3:]
        flag = False
        for w in sec:
            i =  word.find(w)
            if i != -1:
                d = len(w)
                word_1 = word[i:(i + d)]
                word_2 = word[:i]+ word[(i+d):]
                words = [word_1,word_2]
                flag = True
                break

        if flag == False:
            words = [word]
        
        for w in words:
            postag = get_wordnet_pos(w)
            w = stemmer.lemmatize(w, postag)
            if w not in deleted_word:
                word_list.append(w)    
    return word_list


path = "/Users/bingjinliu/Desktop/Erdos Institute/project/playground/pro_desc.csv"
def clean_df(path):
    raw_df = pd.read_csv(path,header = None, skiprows=2)
    refined_df = pd.DataFrame(columns=['file_name','proj_desc'])
    
    for i in raw_df.index:
                if type(raw_df.loc[i,1]) == str:
                    refined_df = refined_df.append({'file_name':raw_df.loc[i,0], 'proj_desc':raw_df.loc[i,1]}, ignore_index= True)
    return refined_df
                    
proj_df = clean_df(path)
print(proj_df.head())
# class MyCorpus:
#     def __iter__(self):
#         for text in proj_df.loc[ : ,'proj_desc'].values:
#             word_list = new_text_preprocess(text)            
#             yield word_list

# 
#memory_friendly_corpus = MyCorpus()

class SecCorpus:
    def __iter__(self):
        with open("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/sector_name/sector_name.txt",'r') as f:
            while True:
                line = f.readline()
                if line:
                    new_line = new_text_preprocess(line)
                    yield new_line
                else:
                    break


sector_corpus = SecCorpus()

# for corpus in memory_friendly_corpus:
#     print(corpus)

num_features = 50
path = "/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/" +str(num_features)+ "-dim_model/refined_common_dic.csv"
dic_df = pd.read_csv(path) 
# print(dic_df.head(1))
#define a function to find the index such that the starting character is different
def divid_index(df):
    index_list = [0]
    N = len(df.index)
    
    for i in range(len(alphabet_string)):
        if i == len(index_list):
            index_list.append(index_list[i-1])
            continue

        for j in range(index_list[i],N):
            if type(df.iloc[j].word) == str:
                char = (df.iloc[j].word)[0]
                if char != alphabet_string[i]:
                    index_list.append(j)
                    break
            # if index_list[i] == N:
    return index_list

# alpha_index_dic = divid_index(dic_df)
# print(alpha_index_dic)
# alpha_index_dic = [0, 1176, 1895, 3353, 4239, 4987, 5548, 5971, 6360, 7052, 7220, 7449, 7993, 8878, 9291, 9694, 10902, 10984, 11921, 13384, 14154, 14470, 14716, 14983, 15039, 15039]
alpha_index_dic=[0, 541, 862, 1570, 1997, 2341, 2619, 2792, 2967, 3261, 3294, 3339, 3580, 3940, 4072, 4250, 4834, 4862, 5340, 6032, 6410, 6555, 6685, 6824, 6825, 6825]
num_features_list = [50,100,300]

def convert_float(list):
    float_list = []
    for string in list:
        float_list.append(float(string))
    return float_list

def doc_embedding_average(dic_df, corpus):
    vecs_0 = []
    vecs_1 = []
    vecs_2 = []
    for doc in corpus:
        num = 0
        sum_0 = np.zeros(num_features_list[0])
        sum_1 = np.zeros(num_features_list[1])
        sum_2 = np.zeros(num_features_list[2])

        for w in doc:
            try:
                l_index = alphabet_string.index(w[0])
            except:
                continue
            else:
                s_index = alpha_index_dic[l_index]
                e_index = alpha_index_dic[l_index + 1] if l_index != 25 else (len(dic_df.index) - 1)
                search_list = list(dic_df.iloc[s_index:e_index].word.to_numpy())
               
                try:
                    w_index = search_list.index(w)
                    
                except:
                    continue
                else:
                    num +=1
                    fls_0 = np.zeros(50)
                    fls_0 = dic_df.iloc[s_index + w_index,0:50].to_numpy()
                    # print(fls_0.shape)
                    # print(sum_0.shape)
                    sum_0 = sum_0 + fls_0

                    line_1 = linecache.getline("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/100-dim_model/refined_common_dic.csv",s_index + w_index +2)
                    ls_1 = line_1.split(",")
                    # print(len(ls_1))
                    # print(ls_1[-1])
                    # print(len(ls_1[0:100]))
                    fls_1 = convert_float(ls_1[0:100])
                    sum_1 =sum_1 + fls_1

                    line_2 = linecache.getline("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/300-dim_model/refined_common_dic.csv", s_index + w_index +2)
                    ls_2 = line_2.split(',')
                    # print(ls_2[-1])
                    
                    fls_2 = convert_float(ls_2[0:300])
                    sum_2 = sum_2 + fls_2
        sum_0 = sum_0/num
        sum_1 = sum_1/num
        sum_2 = sum_2/num
        vecs_0.append(sum_0)
        vecs_1.append(sum_1)
        vecs_2.append(sum_2)
    return vecs_0, vecs_1,vecs_2


def coef_list(topic_num, string):
    coef_list = []
    for i in range(topic_num):
        coef_list.append(string + str(i))
    return coef_list
def construct_vectors_df(vectors,topic_num):
    columns = coef_list(topic_num, 'coef')
    columns.append('file_name')
    coef_df = pd.DataFrame(columns = columns)
    for j in range(len(vectors)):
        vector = vectors[j]
        dic = {'file_name': proj_df.loc[j,'file_name']}
        for i in range(topic_num):
            dic['coef'+str(i)] = round(vector[i],8)
        coef_df = coef_df.append(dic, ignore_index= True)
    return coef_df               
sector_keys = ['agriculture','education','engergy','finance','health','industry','communication','public admin','social protection', 'transportation','water']
def construct_sec_vectors_df(vectors,topic_num):
    columns = coef_list(topic_num, 'coef')
    columns.append('sector')
    coef_df = pd.DataFrame(columns = columns)
    for j in range(len(vectors)):
        vector = vectors[j]
        dic = {'sector': sector_keys[j]}
        for i in range(topic_num):
            dic['coef'+str(i)] = round(vector[i],8)
        coef_df = coef_df.append(dic, ignore_index= True)
    return coef_df 

# vec0,vec1,vec2 = doc_embedding_average(dic_df, memory_friendly_corpus)
# vects = [vec0,vec1,vec2]

# for i in range(3):
#     coef_df = construct_vectors_df(vects[i],num_features_list[i])
#     path = "/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/" + str(num_features_list[i]) +"-dim_model/glove_coef.csv"
#     coef_df.to_csv(path, index = None)

secvec0,secvec1,secvec2 = doc_embedding_average(dic_df, sector_corpus)
secvects = [secvec0,secvec1,secvec2]

for i in range(3):
    coef_df = construct_sec_vectors_df(secvects[i],num_features_list[i])
    path = "/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/" + str(num_features_list[i]) +"-dim_model/refined_sec_glove_coef.csv"
    coef_df.to_csv(path, index = None)