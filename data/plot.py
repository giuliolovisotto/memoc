__author__ = 'giulio'

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import networkx as nx
from sklearn.preprocessing import MinMaxScaler


def euclidean_distance((a, b), (c, d)):
    return math.sqrt((a - c)**2 + (b - d)**2)

pd.set_option('display.mpl_style', 'default')
pd.set_option('display.width', 5000)
plt.rcParams['figure.figsize'] = (15, 8)
pd.set_option('display.max_columns', 60)
plt.ioff()
d = 60
i = 100
m = MinMaxScaler()


G2 = nx.empty_graph(d)
pos2 = np.array(nx.random_layout(G2).values())
pos2 = m.fit_transform(pos2)
plt.scatter(pos2[:, 0], pos2[:, 1], marker='^', s=200)
for i in range(d):
    plt.annotate(i, (pos2[i, 0], pos2[i, 1]))
plt.xlim((-0.05, 1.05))
plt.ylim((-0.05, 1.05))
plt.savefig("rnd_example.png", bbox_inches='tight')
plt.clf()

G3 = nx.barabasi_albert_graph(d, int(math.sqrt(d)))
pos3 = np.array(nx.graphviz_layout(G3, prog='dot').values())
pos3 = m.fit_transform(pos3)
plt.scatter(pos3[:, 0], pos3[:, 1], marker='o', c='r', s=200, )
for i in range(d):
    plt.annotate(i, (pos3[i, 0], pos3[i, 1]))
plt.xlim((-0.05, 1.05))
plt.ylim((-0.05, 1.05))
plt.savefig("cls_example.png", bbox_inches='tight')
plt.clf()

