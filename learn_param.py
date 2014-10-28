#!/bin/python
#Learn the parameters of a Bayesian network for a given structure

from Variable import Variable
from Factor import Factor

def learn_CPT_from_file(data, varCard, parentSets, ess=1.0):
 # varCard: cardinalities of variables
 # parentSets: dictionary of parents of each variable
 # ess: BDe prior equivalent sample size
    
 # create zero-filled CPTs
 N = len(varCard)
 Variables = N*[ None ]
 for i,c in enumerate(varCard):
  Variables[i] = Variable('X'+str(i),c)
 CPT = N*[ None ]
 for i in range(N):
  prior = ess/varCard[i]
  for j in parentSets[i]:
   prior /= varCard[j] 
  CPT[i] = Factor([ Variables[i] ] + [ Variables[j] for j in parentSets[i] ], defaultValue=prior, zeroValue=0)
 # now read count data from file
 for line in data:
  if len(line) == N:
   for i in range(N):
    datum = [line[i]] + [line[j] for j in parentSets[i]]
    CPT[i].incrementValue(datum) # add one
 for i in range(N):
  CPT[i].normalize() 
 return Variables, CPT

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
 var,cpt = learn_CPT_from_file(sys.argv[1],vc,ps,1.0)
 for p in cpt:
  p.printOut()
