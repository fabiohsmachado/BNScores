#!/bin/python
# Read a dataset file (or all dataset files in a given folder) and create all the Kfolds for the Cross Validation.
import os
from Dataset import Dataset

def CreateDatasetDirectory(datasetParentDirectory, dataset):
 if not os.path.exists(datasetParentDirectory):
    os.makedirs(datasetParentDirectory);
 pathToDataset = datasetParentDirectory + "/" + dataset.name;
 if not os.path.exists(pathToDataset):
    os.makedirs(pathToDataset)
 return pathToDataset;

def parse(datasetFile, folds):
 dataset = Dataset();
 dataset.ParseFile(datasetFile);
 datasetPath = CreateDatasetDirectory("parsedFiles", dataset);
 for training, validation in dataset.KFoldGenerator(folds):
  validationFileName = validation.WriteToFile(datasetPath);
  trainingFileName = training.WriteToFile(datasetPath);

def error():
 print "Usage:", sys.argv[0], "data_filename OR data_directory", "number_of_folds";
 exit(0);

if __name__ == "__main__":
 import sys
 if len(sys.argv) < 2:
  error();

 if(os.path.isdir(sys.argv[1])):
  datasetFiles = os.listdir(sys.argv[1]);
  datasetFiles.sort();
  for datasetFile in datasetFiles:
   parse(sys.argv[1] + "/" + datasetFile, int(sys.argv[2]));
 elif(os.path.isfile(sys.argv[1])):
   parse(sys.argv[1], int(sys.argv[2]));
 else:
  error();
