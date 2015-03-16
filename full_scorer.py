#!/bin/python
# Read a dataset file (or all dataset files in a given folder) and create all the Kfolds for the Cross Validation.
import sys, os
from Dataset import Dataset
from create_folds import Parse
from score_files import ScoreFiles
from learn_gobnilp import LearnGobnilp
from learn_twilp import LearnTwilpVariable
from likelihood_gobnilp import GetListOfParents as GetParentsGobnilp
from likelihood_twilp import GetListOfParents as GetParentsTwilp
from data_likelihood import compute_likelihood

def ScoreDatasets(fileList, folds, alpha, parentsLimit):
 for datasetFile in fileList:
  if os.path.isfile(datasetFile):
   dataset = Dataset(datasetFile);
   validationFiles, trainingFiles = Parse(dataset, folds);
   scoreFiles = ScoreFiles(trainingFiles, alpha, parentsLimit);
   GobnilpMatrixFiles, GobnilpResultFiles, GobnilpTimeFiles = LearnGobnilp(scoreFiles);
   treewidths, TwilpYResultFiles, TwilpZResultFiles, TwilpTimeFiles = LearnTwilpVariable(scoreFiles, dataset.variablesQuantity);

   with open(dataset.pathToFiles + "/" + dataset.name + ".result.csv", "w") as resultFile:
    resultFile.write("dataset,fold,treewidth,likelihood,time\n");
    for i, validationFile in enumerate(validationFiles):
     validationDataset = Dataset(validationFile);
     with open(GobnilpTimeFiles[i], "r") as gobnilpTimeFile:
      time = gobnilpTimeFile.readline().split("\t")[1][:-1];
     likelihood = compute_likelihood(validationDataset.data, validationDataset.variablesCardinality, GetParentsGobnilp(GobnilpMatrixFiles[i]), 1);
     resultFile.write(validationDataset.name.split(".")[0] + "," + validationDataset.name.split(".")[1] + ",0," + str(likelihood) + "," + str(time) + "\n");
     print "Likelihood of dataset", validationDataset.name, " using Gobnilp:", likelihood, ", time elapsed: ", time;
     for j, twilpResultFile in enumerate(TwilpZResultFiles[i]):
      with open(TwilpTimeFiles[i][j], "r") as twilpTimeFile:
       time = twilpTimeFile.readline().split("\t")[5][:-1];
      likelihood = compute_likelihood(validationDataset.data, validationDataset.variablesCardinality, GetParentsTwilp(twilpResultFile), 1);
      resultFile.write(validationDataset.name.split(".")[0] + "," + validationDataset.name.split(".")[1] + "," + str(treewidths[j]) + "," + str(likelihood) + "," + str(time) + "\n");
      print "Likelihood of dataset", validationDataset.name, " using Twilp and treewidth", treewidths[j], ": ", str(likelihood), ", time elapsed: ", time;

def Error():
 print "Usage:", sys.argv[0], "data_filename", "number_of_folds", "alpha", "parents_limit";
 exit(0);

if __name__ == "__main__":
 # try:
  ScoreDatasets(sys.argv[1:-1], int(sys.argv[-3]), int(sys.argv[-2]), int(sys.argv[-1]));
 # except:
 #  Error();
