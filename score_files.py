#!/bin/python
#Read a list of datasets and score their variables using Gobnilp's scorer
import sys
import os
from subprocess import call

def ScoreDatasetFile(pathToScorer, pathToDataset, alpha, palim):
 print "Scoring the dataset", pathToDataset;
 scoreFileName = os.path.splitext(pathToDataset)[0] + ".scores";
 scoreCommand = [pathToScorer, pathToDataset, str(alpha), str(palim)];
 with open(scoreFileName, "w") as scoreFile:
  call(scoreCommand, stdout = scoreFile, shell = False);
 print "Finished scoring the dataset", pathToDataset;
 return scoreFileName;

def Error():
 print "Usage:", sys.argv[0], "data_files", "alpha", "parents_limit";
 exit(0);

def ScoreFiles(fileList, alpha, parentsLimit):
 pathToScorer = "/opt/bnet/learning/gobnilp-1.4.1-cplex/scoring"; 
 return [ScoreDatasetFile(pathToScorer, datasetFile, alpha, parentsLimit) for datasetFile in fileList if os.path.isfile(datasetFile)];
 
if __name__ == "__main__":
 try:
  ScoreFiles(sys.argv[1:], int(sys.argv[-2]), int(sys.argv[-1]));
 except:
  Error();
