import networkx as nx
import math
import numpy as np

def save_graph(filename, pos, metric):
    cmat = np.array([np.apply_along_axis(lambda x: metric(x, y), 1, pos) for y in pos])*100
    np.savetxt(filename, cmat, fmt='%f', delimiter=",")


def euclidean_distance((a, b), (c, d)):
    return math.sqrt((a - c)**2 + (b - d)**2)

def manhattan_distance((a, b), (c, d)):
    return abs(a-c) + abs(b-d)


dims = [9, 16, 25, 36, 49, 64]
_dataFolder = 'data'

for d in dims:
    # uniform layout
    G1 = nx.grid_2d_graph(int(math.sqrt(dim)), int(math.sqrt(dim)))
    pos1 = np.array(nx.graphviz_layout(G1, prog='neato').values())
    save_graph("./%s/unif_eucl_%s.csv" % (_dataFolder, d), pos1, euclidean_distance)
    save_graph("./%s/unif_manh_%s.csv" % (_dataFolder, d), pos1, manhattan_distance)
    
    for i in range(20):
        # random layout
        G2 = nx.empty_graph(dim)
        pos2 = np.array(nx.random_layout(G2).values())
        save_graph("./%s/rnd_eucl_%s_%s.csv" % (_dataFolder, d, i), pos2, euclidean_distance)
        save_graph("./%s/rnd_manh_%s_%s.csv" % (_dataFolder, d, i), pos2, manhattan_distance)
        
        # clustered layout
        G3 = nx.barabasi_albert_graph(dim, int(math.sqrt(dim)))
        pos3 = np.array(nx.graphviz_layout(G3, prog='dot').values())
        save_graph("./%s/cls_eucl_%s_%s.csv" % (_dataFolder, d, i), pos3, euclidean_distance)
        save_graph("./%s/cls_manh_%s_%s.csv" % (_dataFolder, d, i), pos3, manhattan_distance)

