__author__ = 'shreyarajpal'

from getProbabilities import priorProb, transitionProb, emissionProb, state, obs

logProb = 20

obsSeq = ''

def getObs(data):
    global obsSeq
    dataFile = open(data,'r')

    for line in dataFile:
        obsSeq += line.rstrip()

    dataFile.close()

    return

def viterbi():
    global logProb
    global obs, obsSeq, state, transitionProb, emissionProb, priorProb

    probMemoization = {j:{i:0 for i in state} for j in xrange(len(obsSeq))}
    previousStateMemoization = {j:{i:0 for i in state} for j in xrange(len(obsSeq))}

    #Initilization
    for i in state:
        probMemoization[0][i] = priorProb[i] + emissionProb[i][obsSeq[0]]
        previousStateMemoization[0][i] = -1 #Stopping condition

    #Viterbi DP
    for i in range(1, len(obsSeq)):
        for currentState in state:
            maxProb = -50000000000000
            maxPrevState = -2
            for previousState in state:
                p = probMemoization[i-1][previousState] + transitionProb[previousState][currentState] + emissionProb[currentState][obsSeq[i]]
                if p>maxProb:
                    maxProb = p
                    maxPrevState = previousState

            probMemoization[i][currentState] = maxProb
            previousStateMemoization[i][currentState] = maxPrevState

    path = []

    currentProbs = probMemoization[len(obsSeq) - 1]

    maxProb = max(currentProbs.values())

    logProb = maxProb

    for j in currentProbs.keys():
        if currentProbs[j]==maxProb:
            maxState = j

    path.append(maxState)

    #Return Viterbi Path
    for i in range(len(obsSeq) - 1, 0, -1):
        prevMaxState = previousStateMemoization[i][maxState]

        path.append(prevMaxState)

        maxState = prevMaxState


    actualPath = []

    for i in range(len(obsSeq) - 1, -1, -1):
        actualPath.append(path[i])

    return actualPath, logProb



def getCpgIslands():
    global logProb

    path, logProb = viterbi()
    islandList = []

    print 'Log-likelihood of most likely assignment is ', logProb,'.'

    statusQuo = False

    start = -1
    end = -1

    for i in xrange(len(path)):
        sign = path[i][1]
        if sign=='-':
            isIsland = False
        else:
            isIsland = True
        if (not statusQuo) and (isIsland):
            statusQuo = True
            start = i + 1
        if (statusQuo) and (not isIsland):
            statusQuo = False
            end = i
            islandList.append((start, end))

    output = file('gene_data/output', 'w')
    start,end = islandList[0]

    output.write(str(start) + ' ' + str(end))

    for i in range(1, len(islandList)):
        item = islandList[i]
        start, end = item
        output.write('\n' + str(start) + ' ' + str(end))

    return islandList

getObs('gene_data/testing.txt')
getCpgIslands()
#print logProb
#print len(obsSeq)
