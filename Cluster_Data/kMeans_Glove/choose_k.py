import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
import os
import matplotlib.pyplot as plt

num_features = 300
path = "/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/" + str(num_features) + "-dim_model/"
os.chdir(path)

sec_df = pd.read_csv("refined_sec_glove_coef.csv")
sec_X = sec_df.iloc[:,0:num_features].to_numpy()
df = pd.read_csv('glove_coef.csv')
doc_X = df.iloc[:, 0:num_features].to_numpy()
X = np.concatenate((doc_X,sec_X), axis = 0)

# initial_centers = sec_df.iloc[:,0:num_features].to_numpy()
possible_ks = range(2,20)
scores = np.zeros(len(possible_ks))
# samples_scores = np.zeros((len(X),len(possible_ks)))
i = 0
for k in possible_ks:
    kmean = KMeans(n_clusters = k, max_iter = 100000)
    y_pred = kmean.fit_predict(X)
    # samples_scores[:,i] = silhouette_samples(X,y_pred)
    scores[i] = silhouette_score(X,y_pred)
    i +=1
print(scores)

plt.figure(figsize = (16,16))
plt.scatter(possible_ks,scores, color = 'blue')
plt.xticks(possible_ks)
plt.xlabel('K')
plt.ylabel('silhouette_score')
plt.savefig('possible_k.png')
# print(samples_scores[0:10,:])



