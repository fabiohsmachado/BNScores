#!/bin/python
# Read a dataset file (or all dataset files in a given folder) and create all the Kfolds for the Cross Validation.
import sys, os
from Dataset import Dataset

def CreateDatasetDirectory(datasetParentDirectory, dataset):
 if not os.path.exists(datasetParentDirectory):
    os.makedirs(datasetParentDirectory);
 pathToDataset = datasetParentDirectory + "/" + dataset.name;
 if not os.path.exists(pathToDataset):
    os.makedirs(pathToDataset)
 return pathToDataset;

def Parse(datasetFile, folds):
 print "Parsing dataset:", datasetFile, "into", folds, "folds.";
 dataset = Dataset();
 dataset.ParseFile(datasetFile);
 datasetPath = CreateDatasetDirectory("datasetFolds", dataset);
 validationFiles = [];
 trainingFiles = [];
 for training, validation in dataset.KFoldGenerator(folds):
  validationFiles.append(validation.WriteToFile(datasetPath));
  trainingFiles.append(training.WriteToFile(datasetPath));
 print "Finished parsing the", datasetFile, "datasetFile.";
 return validationFiles, trainingFiles;

def CreateFolds(fileList, folds):
 results =  [Parse(datasetFile, folds) for datasetFile in fileList if os.path.isfile(datasetFile)];
 validationFiles, trainingFiles =  [[row[i] for row in results] for i in range(len(results))]
 return validationFiles, trainingFiles;

def Error():
 print "Usage:", sys.argv[0], "data_filename", "number_of_folds";
 exit(0);

if __name__ == "__main__":
 try:
  print CreateFolds(sys.argv[1:-1], int(sys.argv[-1]));
 except:
  Error();
