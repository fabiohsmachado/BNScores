import math
import os
from random import shuffle

class Dataset:
 def __init__(self):
  self.data = [];
  self.variablesQuantity = 0;
  self.variablesCardinality = [];
  self.name = "";

def ParseFile(filename):
 dataset = Dataset();
 name = os.path.basename(filename);
 dataset.name = os.path.splitext(name)[0];

 with open(filename, "r") as datasetFile:
  dataset.variablesQuantity = int(datasetFile.readline());
  dataset.variablesCardinality = datasetFile.readline().strip('\n');
  datasetFile.readline();
  for line in datasetFile:
   dataset.data.append(line);
  return dataset;

def CloneDatasetWithoutData(dataset):
 cloneDataset = Dataset();
 cloneDataset.name = dataset.name;
 cloneDataset.variablesQuantity = dataset.variablesQuantity;
 cloneDataset.variablesCardinality = dataset.variablesCardinality;
 return cloneDataset;

def KFoldCrossValidation(dataset, K, randomise = True):
 data = dataset.data;
 if randomise:
  data = list(data);
  shuffle(data);
 
 training = CloneDatasetWithoutData(dataset);
 validation = CloneDatasetWithoutData(dataset);
 dataPerFold = math.ceil(len(data) / K);

 for k in xrange(K):
  training.data = [line for i, line in enumerate(data) if math.floor(i/dataPerFold) != k]
  training.name = dataset.name + "." + str(k) + ".training";
  validation.data = [line for i, line in enumerate(data) if math.floor(i/dataPerFold) == k]
  validation.name = dataset.name + "." + str(k) + ".validation";
  yield training, validation;

def CreateDatasetDirectory(datasetParentDirectory, dataset):
 if not os.path.exists(datasetParentDirectory):
    os.makedirs(datasetParentDirectory);

 pathToDataset = datasetParentDirectory + "/" + dataset.name;
 if not os.path.exists(pathToDataset):
    os.makedirs(pathToDataset)

 return pathToDataset;

def WriteDatasetToFile(path, dataset):
 with open(path + "/" + dataset.name + ".data", "w") as datasetFile:
  datasetFile.write(str(dataset.variablesQuantity) + "\n");
  datasetFile.write(dataset.variablesCardinality + "\n");
  datasetFile.write(str(len(dataset.data)) + "\n");
  for dataLine in dataset.data:
   datasetFile.write(dataLine);

def main():
 dataset = ParseFile("files/nursery_bin.data");
 datasetPath = CreateDatasetDirectory("parsedFiles", dataset);
 for training, validation in KFoldCrossValidation(dataset, 10):
  WriteDatasetToFile(datasetPath, training);
  WriteDatasetToFile(datasetPath, validation);

    # TODO:
    # OK: Create dataset class
    # OK: Parse file and create a dataset object
    # OK: Cross validate the dataset into subdatasets
    # OK: Creat subdirectory structure
    # OK: Save the subdataset to files
    # Run scoring in each training dataset
    # Run gobnilp foreach score file
    # Run twilp for each score file
    # Create BNTree class
    # Parser gobnilp result and create a BNTree instance
    # Parser twilp result and create another BNTree instance
    # Apply MLE in the test instances of datasets with the Gobnilp BNTree
    # Apply MLE in the test instances of datasets with the Twilp BNTree

if __name__ == "__main__":
 main();
