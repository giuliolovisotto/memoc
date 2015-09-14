import networkx as nx
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler

m = MinMaxScaler()

def save_graph(filename, pos, metric):
    cmat = np.array([np.apply_along_axis(lambda x: metric(x, y), 1, pos) for y in pos])
    np.savetxt(filename, cmat, fmt='%.8f', delimiter=",")


def euclidean_distance((a, b), (c, d)):
    return math.sqrt((a - c)**2 + (b - d)**2)

def manhattan_distance((a, b), (c, d)):
    return abs(a-c) + abs(b-d)


dims = [5, 10, 20, 40, 60]
_dataFolder = 'datasets'

for d in dims:
    # uniform layout
    G1 = nx.grid_2d_graph(int(math.sqrt(d)), int(math.sqrt(d)))
    pos1 = np.array(nx.graphviz_layout(G1, prog='neato').values())
    pos1 = m.fit_transform(pos1)
    save_graph("./%s/uni_eucl_%s_0.csv" % (_dataFolder, d), pos1, euclidean_distance)
    save_graph("./%s/uni_manh_%s_0.csv" % (_dataFolder, d), pos1, manhattan_distance)
    
    for i in range(20):
        # random layout
        G2 = nx.empty_graph(d)
        pos2 = np.array(nx.random_layout(G2).values())
        pos2 = m.fit_transform(pos2)

        save_graph("./%s/rnd_eucl_%s_%s.csv" % (_dataFolder, d, i), pos2, euclidean_distance)
        save_graph("./%s/rnd_manh_%s_%s.csv" % (_dataFolder, d, i), pos2, manhattan_distance)
        
        # clustered layout
        G3 = nx.barabasi_albert_graph(d, int(math.sqrt(d)))
        pos3 = np.array(nx.graphviz_layout(G3, prog='dot').values())
        pos3 = m.fit_transform(pos3)

        save_graph("./%s/cls_eucl_%s_%s.csv" % (_dataFolder, d, i), pos3, euclidean_distance)
        save_graph("./%s/cls_manh_%s_%s.csv" % (_dataFolder, d, i), pos3, manhattan_distance)

