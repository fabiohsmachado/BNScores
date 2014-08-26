# Implements Dataset class
# 
import math
import os
from random import shuffle

class Dataset:
 """ Class Dataset """
 def __init__(self):
  self.data = [];
  self.variablesQuantity = 0;
  self.variablesCardinality = "";
  self.name = "";

 def ParseFile(self, filename):
  self.name = os.path.splitext(os.path.basename(filename))[0];
  with open(filename, "r") as datasetFile:
   self.variablesQuantity = int(datasetFile.readline());
   self.variablesCardinality = datasetFile.readline().strip('\n');
   datasetFile.readline();
   for line in datasetFile:
    self.data.append(line);

 def CloneWithoutData(self):
  cloneDataset = Dataset();
  cloneDataset.name = self.name;
  cloneDataset.variablesQuantity = self.variablesQuantity;
  cloneDataset.variablesCardinality = self.variablesCardinality;
  return cloneDataset;

 def KFoldGenerator(self, K, randomise = True):
  data = self.data;
  if randomise:
   data = list(data);
   shuffle(data);
 
  training = self.CloneWithoutData();
  validation = self.CloneWithoutData();
  dataPerFold = math.ceil(len(data) / K);

  for k in xrange(K):
   training.data = [line for i, line in enumerate(data) if math.floor(i/dataPerFold) != k]
   training.name = self.name + "." + str(k) + ".training";
   validation.data = [line for i, line in enumerate(data) if math.floor(i/dataPerFold) == k]
   validation.name = self.name + "." + str(k) + ".validation";
   yield training, validation;

 def WriteToFile(self, path = "./"):
  datasetFileName = path + "/" + self.name + ".data";
  with open(datasetFileName, "w") as datasetFile:
   datasetFile.write(str(self.variablesQuantity) + "\n");
   datasetFile.write(self.variablesCardinality + "\n");
   datasetFile.write(str(len(self.data)) + "\n");
   for dataLine in self.data:
    datasetFile.write(dataLine);
  return datasetFileName;
