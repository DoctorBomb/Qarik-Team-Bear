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



# def text_preprocess(text):
#     '''
#     Remove all punctuation,stopwords, lemmatize -> returns list of words
#     '''
#     word_list =[]
#     nopunc = re.sub(r'[^a-zA-Z]',' ',text)
#     nopunc = [w.lower() for w in nopunc.split()]
#     for word in nopunc:
#         if word != 'and' and str.find('and', word) == 0:
#                 word = word[3:]
#         word = stemmer.lemmatize(word, get_wordnet_pos(word))
#         if word not in deleted_word:
#             word_list.append(word)    
#     return word_list


# sector_keys = ['agriculture','education','engergy','finance','health','industry','communication','public admin','social protection','water', 'transportation']
# sector_values = []
# with open("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/sector_name/sector_name.txt",'r') as f:
#     while True:
#         line = f.readline()
#         if line:
#             new_line = text_preprocess(line)
#             sector_values.append(new_line)
#         else:
#             break

# sec = []
# for sector in sector_values:
#     for x in sector:
#         if x not in sec:
#             sec.append(x) 
# for sector in sector_keys:
#     sector = text_preprocess(sector)[0]
#     if sector not in sec:
#             sec.append(sector) 

# with open("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/sector_name/sector.txt",'w') as f:
#     for word in sec:
#         f.write(word + '\n')


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
                word_list.append((w,postag))    
    return word_list

raw_df = pd.read_csv("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/pro_desc.csv",header = None, skiprows=2)


class MyCorpus:
    def __iter__(self):
        for text in raw_df.loc[:,1].values:
            if type(text) != str:
                continue
            word_list = new_text_preprocess(text)
            yield word_list

memory_friendly_corpus = MyCorpus()


frequency = defaultdict(int)
for file in memory_friendly_corpus:
    for token in file:
        frequency[token] += 1


dic_df = pd.DataFrame(columns= ['word', 'freq', 'in_words','postag'])
for token, freq in frequency.items():
    if token[0] == '' or type(token[0]) != str:
        continue
    elif (token[0] in words) or (token[0] in sec):
        dic_df = dic_df.append({'word': token[0], 'freq': freq, 'in_words': 1, 'postag':token[1]}, ignore_index= True)
    else:
        dic_df = dic_df.append({'word': token[0], 'freq': freq, 'in_words': 0, 'postag':token[1]}, ignore_index= True)

dic_df.to_csv("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/dictionaries/refined_dic.csv", index=False)
# # dictionary.token2id
