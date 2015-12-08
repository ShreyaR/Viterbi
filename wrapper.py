__author__ = 'shreyarajpal'

import sys

from Viterbi import getObs, getCpgIslands, viterbi, obsSeq
from getProbabilities import priorProb, emissionProb, transitionProb, getEmissionProbs, getTransitionAndPriorProbs

training = sys.argv[1]
training_cpgIslands = sys.argv[2]
test = sys.argv[3]

logProb = 500

getTransitionAndPriorProbs(training, training_cpgIslands)
getEmissionProbs()
getObs(test)
getCpgIslands()

