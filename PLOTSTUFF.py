__author__ = 'giulio'
# now lets generate plots
import matplotlib.pyplot as plt
import pandas as pd
import os
import os.path
import numpy as np


pd.set_option('display.mpl_style', 'default')
pd.set_option('display.width', 5000)
plt.rcParams['figure.figsize'] = (15, 8)
pd.set_option('display.max_columns', 60)
plt.ioff()
def getInfo(filename):
    fn = filename[:-4]  # remove extension
    return fn.split('_')  #

# 1. plot, sulle x le sizes, sulle y i tempi di esecuzione average sulle varie istanze, una serie per ogni metodo e distanza.

# 2 metodi (cplex, pso)
# 2 distanze (eucl, manh)

dFolder = "data/datasets/"

datasets = [ f for f in os.listdir(dFolder) if os.path.isfile(os.path.join(dFolder, f)) ]

datasets = filter(lambda x: x[-4:] == ".csv", datasets)

dims = sorted(map(lambda x: int(x.split('_')[2]), datasets))

# this is a matrix that in every column has a series of dims elements

plot_vals = np.zeros((len(dims), 0))
plot_names = list()


for m in ['cplex', 'pso']:
    rFolder = "./results/%s/" % m
    datasets = [ f for f in os.listdir(rFolder) if os.path.isfile(os.path.join(rFolder, f)) ]
    datasets = filter(lambda x: x[-4:] == ".csv", datasets)
    for dm in ['eucl', 'manh']:
        # filter with distance measure
        s = filter(lambda x: dm in x, datasets)

        resM = np.zeros(len(dims))
        stdM = np.zeros(len(dims))
        for k, dim in enumerate(dims):
            # filter with dimensionality
            t = filter(lambda x: int(getInfo(x)[2]) == dim, s)
            # now in t we have only datasets with dm, and dimensionality dim
            res = np.zeros(len(t))
            for i, f in enumerate(t):
                res[i] = np.loadtxt(rFolder + f, delimiter=",", )[0]

            resM[k] = res.mean()
            stdM[k] = res.std()

        plot_vals = np.hstack((plot_vals, resM[:, None]))
        plot_names.append("%s_%s" % (m, dm))


df = pd.DataFrame(plot_vals, columns=plot_names)

df.plot(kind='line', logy=True, linewidth=2, colormap='rainbow')
plt.xlabel("nodes")
plt.ylabel("time")
plt.show()

plt.clf()

# 1. plot, sulle x le sizes, sulle y i tempi di esecuzione average sulle varie istanze, una serie per ogni metodo e
# tipo di punti.

# 2 metodi (cplex, pso)
# 3 tipi di punti (uni, rnd, cls)

plot_vals = np.zeros((len(dims), 0))
plot_names = list()

for m in ['cplex', 'pso']:
    rFolder = "./results/%s/" % m
    datasets = [ f for f in os.listdir(rFolder) if os.path.isfile(os.path.join(rFolder, f)) ]
    datasets = filter(lambda x: x[-4:] == ".csv", datasets)
    for pt in ['uni', 'rnd', 'cls']:
        # filter with distance measure
        s = filter(lambda x: pt in x, datasets)
        resM = np.zeros(len(dims))
        stdM = np.zeros(len(dims))
        for k, dim in enumerate(dims):
            # filter with dimensionality
            t = filter(lambda x: int(getInfo(x)[2]) == dim, s)
            # now in t we have only datasets with pt, and dimensionality dim
            res = np.zeros(len(t))
            for i, f in enumerate(t):
                res[i] = np.loadtxt(rFolder + f, delimiter=",", )[0]

            resM[k] = res.mean()
            stdM[k] = res.std()

        plot_vals = np.hstack((plot_vals, resM[:, None]))
        plot_names.append("%s_%s" % (m, pt))


df = pd.DataFrame(plot_vals, columns=plot_names)

df.plot(kind='line', logy=True, linewidth=2, colormap='rainbow')
plt.xlabel("nodes")
plt.ylabel("time")
plt.show()

plt.clf()

# 3. plot sulle x le sizes sulle y l'errore di pso sull'ottimo trovato da cplex con stdbars

plot_vals = np.zeros((len(dims), 0))
plot_errors = np.zeros((len(dims), 0))
plot_names = list()


def get_opt(filename):
    return np.loadtxt("./cplex/%s_%s_%s_%s.csv" % filename[:-4].split("_"), delimiter=",")[0]

for m in ['pso']:
    rFolder = "./results/%s/" % m
    datasets = [ f for f in os.listdir(rFolder) if os.path.isfile(os.path.join(rFolder, f)) ]
    datasets = filter(lambda x: x[-4:] == ".csv", datasets)
    resM = np.zeros(len(dims))
    stdM = np.zeros(len(dims))
    for k, dim in enumerate(dims):
        # filter with dimensionality
        t = filter(lambda x: int(getInfo(x)[2]) == dim, datasets)
        # now in t we have only datasets with dimensionality dim
        res = np.zeros(len(t))
        for i, f in enumerate(t):
            best_for_m = np.loadtxt(rFolder + f, delimiter=",", )[0]
            optimum = get_opt(f)
            res[i] = (best_for_m - optimum)/float(optimum)
        resM[k] = res.mean()
        stdM[k] = res.std()
    plot_vals = np.hstack((plot_vals, resM[:, None]))
    plot_errors = np.hstack((plot_errors, stdM[:, None]))
    plot_names.append(m)


df = pd.DataFrame(plot_vals, columns=plot_names)

df.plot(kind='line', yerr=plot_errors, linewidth=2, colormap='rainbow')

# plt.errorbar(x, y, e, linestyle='None', marker='^')

plt.xlabel("nodes")
plt.ylabel("error %")
plt.show()

plt.clf()

# plt.savefig("%s/%s_feat.png" % (fold, f[:-4]), bbox_inches='tight')
#plt.ylim(min(d['std'].min()-1, d['mean'].min()-1), max(d['std'].max()+1, d['mean'].max()+1))


