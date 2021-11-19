import matplotlib.pyplot as plt
import pandas as pd
import os

num_features = 300
num_doc = 2940

path = "/Users/bingjinliu/Desktop/Erdos Institute/project/playground/doc2vec/" + str(num_features) + "-dim_model/"
os.chdir(path)

COLORS = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan','k']
sector_keys = ['agriculture','education','engergy','finance','health','industry','communication','public admin','social protection','water', 'transportation']

df = pd.read_csv('refined_glove_sec_tnes.csv')
plt.ion()
plt.figure(figsize=(10,10))

for i in range(num_doc):
    plt.scatter(df.loc[i,'x'],df.loc[i,'y'],c = 'tan', s = 10)

for j in range(11):
    index = j + num_doc
    plt.scatter(df.loc[index, 'x'], df.loc[index,'y'] , c = COLORS[j], label = sector_keys[j])

plt.legend()
plt.draw()
plt.savefig("refined_glove_sec_tnes.png")

# plt.scatter([0,1],[1,5], c = COLORS[0])
# plt.show()
