from sklearn.manifold import TSNE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

sector_keys = ['agriculture','education','engergy','finance','health','industry','communication','public admin','social protection','water', 'transportation']
num_features = 300
path = "/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/" + str(num_features) + "-dim_model/"
os.chdir(path)
vectors_df = pd.read_csv("glove_coef.csv")
sector_df = pd.read_csv('refined_sec_glove_coef.csv')

X_doc = np.array(vectors_df.iloc[:,0:num_features])
X_sec = np.array(sector_df.iloc[:,0:num_features])
# print(X_sec.shape)
X = np.concatenate((X_doc, X_sec), axis = 0)

t_sne = TSNE(n_components = 2)
X_tsne = t_sne.fit_transform(X)
index = np.concatenate((vectors_df.file_name.to_numpy(),sector_keys), axis = 0)

df = pd.DataFrame(X_tsne, index = index, columns = ['x', 'y'])
print(df.head())
df.to_csv("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/300-dim_model/refined_glove_sec_tnes.csv")


