#!/bin/python
#Compute the data likelihood for a give network structure

from Variable import Variable
from Factor import Factor
from learn_param import learn_CPT_from_file
from math import log

def compute_likelihood(data, varCard, parentSets, ess):
 # varCard: cardinalities of variables
 # parentSets: dictionary of parents of each variable
 # ess: BDe prior equivalent sample size
    
 N = len(varCard)
 # learn network from file
 Variables, CPT = learn_CPT_from_file(data, varCard, parentSets, ess)
 # use learned network to compute log likelihoods
 loglik = 0.0
 for line in data:
  if len(line) == N:
   for i in range(N):
    datum = [line[i]] + [line[j] for j in parentSets[i]]
    loglik += log(CPT[i].getValue(datum))
 return loglik

if __name__ == '__main__':
 import sys, time
 if len(sys.argv) < 1:
  print "Usage:", sys.argv[0], "data_filename"
  exit(0)
 # A <- B, C
 # B <- C
 # C <-
 vc = [ 2, 2, 2 ]
 ps = [ [1,2], [2], [] ]
 print 'Likelihood:', compute_likelihood(sys.argv[1],vc,ps,1.0)
