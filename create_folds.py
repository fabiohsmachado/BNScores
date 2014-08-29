#!/bin/python
# Read a dataset file (or all dataset files in a given folder) and create all the Kfolds for the Cross Validation.
import sys, os
from glob import glob
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
 validationFiles = [];
 trainingFiles = [];
 for training, validation in dataset.KFoldGenerator(folds):
  validationFiles.append(validation.WriteToFile(datasetPath));
  trainingFiles.append(training.WriteToFile(datasetPath));
 return validationFiles, trainingFiles;

def error():
 print "Usage:", sys.argv[0], "data_filename", "number_of_folds";
 exit(0);

def main():
 if len(sys.argv) < 3:
  error();

 for datasetFile in glob(sys.argv[1]):
  if os.path.isfile(datasetFile):
   parse(datasetFile, int(sys.argv[2]));

if __name__ == "__main__":
 main();
