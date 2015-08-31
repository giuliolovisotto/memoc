from subprocess import call
import os
import os.path
import numpy as np

methods = {
    "cplex": 'cplex/cplex',
    "pso": 'heur/pso'
}

dFolder = "data/datasets/"

datasets = [ f for f in os.listdir(dFolder) if os.path.isfile(os.path.join(dFolder, f)) ]

datasets = filter(lambda x: x[-4:] == ".csv", datasets)

def getInfo(filename):
    fn = filename[:-4]  # remove extension
    return fn.split('_')  # 

for d in datasets:
    print d
    n = int(getInfo(d)[2])
    k = int(getInfo(d)[3])
    m = getInfo(d)[1]
    t = getInfo(d)[0]

    # cplex first
    times = 5
    # first column is time, second is objval, others are path
    res = np.zeros((times, 2))
    
    for i in range(times):
        call([methods['cplex'], os.path.join(dFolder, d)])
        res[i] = np.loadtxt("results.csv", delimiter=',')
        os.remove("results.csv")
    np.savetxt("results/%s/%s" % ('cplex', d), res[:, :2].mean(axis=0))
    print "cplex: %s, %s" % (res[:, :2].mean(axis=0)[0], res[:, :2].mean(axis=0)[1])
    
    # now pso
    # first column is time, second is objval, others are path
    for i in range(times):
        call([methods['pso'], os.path.join(dFolder, d)])
        res[i] = np.loadtxt("results.csv", delimiter=',')
        os.remove("results.csv")
    np.savetxt("results/%s/%s" % ('pso', d), res[:, :2].mean(axis=0))
    print "pso: %s, %s" % (res[:, :2].mean(axis=0)[0], res[:, :2].mean(axis=0)[1])






