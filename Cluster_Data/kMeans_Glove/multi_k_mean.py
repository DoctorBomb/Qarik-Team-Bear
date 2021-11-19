from sklearn.cluster import KMeans
import os
import pandas as pd
import numpy as np

## gather data
num_features = 300

sec_df = pd.read_csv("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/300-dim_model/refined_sec_glove_coef.csv")
sec_X = sec_df.iloc[:,0:num_features].to_numpy()
sector_names = ['agriculture','education','engergy','finance','health','industry','communication','public admin','social protection', 'transportation','water']

df = pd.read_csv("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/300-dim_model/glove_coef.csv")
doc_X = df.iloc[:, 0:num_features].to_numpy()
file_names = df['file_name'].to_numpy().reshape(-1,1)
doc_size = 2940


#doing 100 times k_mean
X = np.concatenate((doc_X,sec_X), axis = 0)


def freq_vec(num_trails):
    ## rows are index of documents, the first 11 columns are index of sectors, and the last column means the doc is not in any section
    freq = np.zeros((doc_size, 12))
    for i in range(num_trails):
        kmean = KMeans(n_clusters=11, max_iter = 10000)
        y = kmean.fit_predict(X)
        doc_y = y[0:doc_size]
        # print(doc_y[0])
        sec_y = y[doc_size:]
        # print(sec_y)
        dic = {}
        for j in range(11):
            indx = list(np.where(sec_y == j)[0])
            if len(indx) != 0:
                dic[j] = indx
            else:
                dic[j] = [11]
        for k in range(doc_size):
            sec = dic[doc_y[k]]
            for s in range(len(sec)):
                freq[k,sec[s]] += 1/len(sec)
    freq = freq/num_trails
    return freq
            
freq = freq_vec(500)
sector_names.append('not_classified')
sector_names.insert(0,'file_name')

vec = np.concatenate((file_names,freq),axis = 1)
freq_df = pd.DataFrame(vec, columns = sector_names)
# print(freq_df.iloc[0,1:13])
freq_df.to_csv("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/300-dim_model/freq.csv")