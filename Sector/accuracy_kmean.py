import pandas as pd
import os

from pandas.io.parsers import read_csv

num_features = 300
path = "/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/" + str(num_features) + "-dim_model/"
os.chdir(path)
label_df = pd.read_csv("refined_kmean_cluster.csv")
proj_df = read_csv("/Users/bingjinliu/Desktop/Erdos Institute/project/playground/pro_desc.csv")
sec_df = pd.read_csv('refined_sec_kmean_cluster.csv')
print(label_df.cluster_label.value_counts())

nt_classifed_df = pd.DataFrame(columns=['file_name','proj_desc'])

for i in range(11):
    files_df = label_df.loc[label_df.cluster_label == i]
    names = files_df.sample(1)['file_name'].to_numpy()
    sector = sec_df.loc[sec_df.cluster_label == i,'sector'].values
    if sector.size == 0:
        sector = "No such sectors"
        for n_name in files_df['file_name'].to_numpy():
            dic ={}
            dic['file_name'] = n_name
            dic['proj_desc'] = proj_df.loc[proj_df.iloc[:,0] == n_name,'proj_desc'].values
            nt_classifed_df = nt_classifed_df.append(dic, ignore_index=True)
        

    print("************************" + sector + "************************")

    for name in names:
        print(name)
        try:
            print(proj_df.loc[proj_df.iloc[:,0] == name,'proj_desc'].values)   
        except:
            print('No such file founded')

nt_classifed_df.to_csv('not_classifed.csv', index=None)    