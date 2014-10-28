#!/bin/python
# Read a dataset file (or all dataset files in a given folder) and create all the Kfolds for the Cross Validation.
import sys, os
from create_folds import Parse
from score_files import ScoreFiles
from learn_gobnilp import LearnGobnilp
from learn_twilp import LearnTwilp

def ScoreDatasets(fileList, folds, alpha, parentsLimit, treewidth):
 for datasetFile in fileList:
  if os.path.isfile(datasetFile):
    validationFiles, trainingFiles = Parse(datasetFile, folds);
    scoreFiles = ScoreFiles(trainingFiles, alpha, parentsLimit);
    GobnilpMatrixFiles, GobnilpResultFiles, GobnilpTimeFiles = LearnGobnilp(scoreFiles);
 # LearnGobnilp(ScoreFiles);

def Error():
 print "Usage:", sys.argv[0], "data_filename", "number_of_folds", "alpha", "parents_limit", "treewidth";
 exit(0);

if __name__ == "__main__":
 # try:
  ScoreDatasets(sys.argv[1:-1], int(sys.argv[-4]), int(sys.argv[-3]), int(sys.argv[-2]), int(sys.argv[-1]));
 # except:
 #  Error();
