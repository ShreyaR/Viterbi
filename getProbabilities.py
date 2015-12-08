__author__ = 'shreyarajpal'

from math import exp,log

state = ['A+', 'G+', 'C+', 'T+', 'A-', 'G-', 'C-', 'T-']
obs = ['A', 'G', 'C', 'T']
islands = []

nearZero = exp(-15)

transitionCount = {x:{y:nearZero for y in state} for x in state}
transitionProb = {x:{y:nearZero for y in state} for x in state}
emissionProb = {x:{y:nearZero for y in obs} for x in state}

priorCount = {x:nearZero for x in state}
priorProb = {x:nearZero for x in state}

def inIsland(i):
    for x in islands:
        start,end = x
        if i>=start and i<= end:
            return '+'
    return '-'

def getTransitionAndPriorProbs(file, cpg):
    global islands
    global transitionCount, transitionProb, priorCount, priorProb

    data = open(file,'r')
    cpg_islands = open(cpg, 'r')

    for line in cpg_islands:
        start,end = [int(i) for i in line.rstrip().split(' ')]
        islands.append((start, end))

    count = 0
    startBase = 0
    for line in data:
        line = line.rstrip()
        for i in line:
            count += 1
            flag = inIsland(count)
            base = i + flag
            if count == 1:
                startBase = base
                if flag=='-':
                    priorCount[i+flag] += 1
                continue
            else:
                transitionCount[startBase][base] += 1
                startBase = base
                if flag=='-':
                    priorCount[i+flag] += 1

    for i in transitionCount.keys():
        z = sum(transitionCount[i].values())
        for j in transitionCount[i].keys():
            transitionProb[i][j] = transitionCount[i][j]/float(z)

    z = sum(priorCount.values())
    for i in priorCount.keys():
        priorProb[i] = priorCount[i]/float(z)

    data.close()
    cpg_islands.close()
    return

def getEmissionProbs():
    global emissionProb

    for i in emissionProb.keys():
        desiredObs = i[0]
        emissionProb[i][desiredObs] = 1

#def getTransitionProb():
#transFormDataset('gene_data/training.txt', 'gene_data/cpg_island_training.txt')
getTransitionAndPriorProbs('gene_data/training.txt', 'gene_data/cpg_island_training.txt')
getEmissionProbs()
#print inIsland(583)

#print transitionProb
#print transitionCount
#print priorCount
#print priorProb
#print emissionProb

for i in transitionProb.keys():
    for j in transitionProb[i].keys():
        transitionProb[i][j] = log(transitionProb[i][j])

for i in emissionProb.keys():
    for j in emissionProb[i].keys():
        emissionProb[i][j] = log(emissionProb[i][j])

for i in priorProb.keys():
    priorProb[i] = log(priorProb[i])

#print transitionProb
#print transitionCount
#print priorCount
#print priorProb
#print emissionProb