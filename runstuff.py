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

datasets = sorted(filter(lambda x: x[-4:] == ".csv", datasets))

# remove already present results

cplex_done_already = [ f for f in os.listdir("results/cplex/") if os.path.isfile(os.path.join("results/cplex/", f)) ]
pso_done_already = [ f for f in os.listdir("results/pso/") if os.path.isfile(os.path.join("results/pso/", f)) ]

done_already = set(cplex_done_already) & set(pso_done_already)

datasets = sorted(list(set(datasets) - done_already))

print "%s datasets to process\n%s datasets already done\n" % (len(datasets), len(done_already))

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
    
    optimums = {}
    
    for i in range(times):
        call([methods['cplex'], os.path.join(dFolder, d)])
        res[i] = np.loadtxt("results.csv", delimiter=',')
        os.remove("results.csv")
    np.savetxt("results/%s/%s" % ('cplex', d), res[:, :2].mean(axis=0))
    optimums[d] = res[:, 1].mean()
    print "cpx: %s, %s" % (res[:, :2].mean(axis=0)[0], res[:, :2].mean(axis=0)[1])
    
    # now pso
    res = np.zeros((times, 2))
    objf = np.zeros((times, 500))
    # first column is time, second is objval, third is error wrt optimum
    for i in range(times):
        call([methods['pso'], os.path.join(dFolder, d)])
        rfile = np.loadtxt("results.csv", delimiter=',')
        res[i] = rfile[:2]
        objf[i] = rfile[2:]
        opts = np.tile(optimums[d], objf.shape[1])
        objf[i] = (objf[i]-opts)/opts
        os.remove("results.csv")
    np.savetxt("results/%s/%s" % ('pso', d), np.hstack((res[:, :2], objf)).mean(axis=0))
    print "pso: %s, %s" % (res[:, :2].mean(axis=0)[0], res[:, :2].mean(axis=0)[1])






