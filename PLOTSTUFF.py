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

dims = sorted(set(map(lambda x: int(x.split('_')[2]), datasets)))

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


df = pd.DataFrame(plot_vals, index=np.array(dims), columns=plot_names)
df.plot(kind='line', logy=True, linewidth=2, colormap='rainbow', marker='^')
plt.xlabel("numero di nodi", fontsize=18)
plt.ylabel("tempo di esecuzione (s)", fontsize=18)
plt.xlim((0, 65))
# We change the fontsize of minor ticks label
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)
plt.savefig("report/Figures/uno.png", bbox_inches='tight')
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


df = pd.DataFrame(plot_vals, index=np.array(dims), columns=plot_names)
df.plot(kind='line', logy=True, linewidth=2, colormap='rainbow', marker='^')
plt.xlim((0, 65))
plt.xlabel("numero di nodi", fontsize=18)
plt.ylabel("tempo di esecuzione (s)", fontsize=18)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)
plt.savefig("report/Figures/due.png", bbox_inches='tight')
plt.clf()

# 3. plot sulle x le sizes sulle y l'errore di pso sull'ottimo trovato da cplex con stdbars
plot_vals = np.zeros((len(dims), 0))
plot_errors = np.zeros((len(dims), 0))
plot_names = list()

def get_opt(filename):
    return np.loadtxt("./results/cplex/%s_%s_%s_%s.csv" % tuple(filename[:-4].split("_")), delimiter=",")[0]

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
            res[i] = np.loadtxt(rFolder + f, delimiter=",", )[-1:]
        resM[k] = res.mean()
        stdM[k] = res.std()
    plot_vals = np.hstack((plot_vals, resM[:, None]))
    plot_errors = np.hstack((plot_errors, stdM[:, None]))
    plot_names.append(m)

df = pd.DataFrame(np.abs(plot_vals), index=np.array(dims), columns=plot_names)
df_error = pd.DataFrame(np.abs(plot_errors), index=np.array(dims), columns=plot_names)
df.plot(kind='line', legend=True, linewidth=3)
plt.errorbar(np.array(dims), plot_vals, plot_errors, ecolor='black', linestyle='b', marker='o', elinewidth=2,)
plt.xlabel("numero di nodi", fontsize=18)
plt.xlim((0, 65))
plt.ylabel("errore (%)", fontsize=18)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)
plt.savefig("report/Figures/tre.png", bbox_inches='tight')
plt.clf()

# 4, plot sulle x le iterations di pso, sulle y una serie per ogni dimensionalita, con i valori che sono l'errore percentuale sull'ottimo a quel punto

iterations = 500
rFolder = "results/pso/"
datasets = [ f for f in os.listdir(rFolder) if os.path.isfile(os.path.join(rFolder, f)) ]
datasets = filter(lambda x: x[-4:] == ".csv", datasets)
resM = np.zeros((len(dims), iterations))
stdM = np.zeros((len(dims), iterations))
plot_names = list()
for k, dim in enumerate(dims):
    # filter with dimensionality
    t = filter(lambda x: int(getInfo(x)[2]) == dim, datasets)
    # now in t we have only datasets with dimensionality dim
    res = np.zeros((len(t), iterations))
    for i, f in enumerate(t):
        res[i] = np.loadtxt(rFolder + f, delimiter=",", )[2:]
    resM[k] = res.mean(axis=0)
    stdM[k] = res.std(axis=0)
    plot_names.append(dim)

plot_vals = resM.T
plot_errors = stdM.T

df = pd.DataFrame(plot_vals, columns=plot_names)
df.plot(kind='line', linewidth=2, colormap='rainbow')
# prendiamo 5 punti per plottare i markers
indici = (np.array([0,1,2,3,4,4.99])*100).astype(int)
xs = np.arange(500)[indici]
ys = plot_vals[indici, :]
styles = ['s', 'D', '^', '*', 'o']
colors = ['purple', 'dodgerblue', 'springgreen', 'orange', 'red']
for l in range(plot_vals.shape[1]):
    plt.plot(xs, ys[:, l], marker=styles[l], color=colors[l], lw=0)

# plt.errorbar(df.index, plot_vals, plot_errors, ecolor='black', linestyle='b', marker='o', elinewidth=2,)
plt.xlabel("iterazioni", fontsize=18)
plt.ylabel("errore (%)", fontsize=18)
plt.legend(title="numero di nodi")
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)
plt.savefig("report/Figures/quattro.png", bbox_inches='tight')
plt.clf()

