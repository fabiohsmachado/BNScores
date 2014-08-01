import math
import os
from random import shuffle
from subprocess import call

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
 datasetFileName = path + "/" + dataset.name + ".data";
 with open(datasetFileName, "w") as datasetFile:
  datasetFile.write(str(dataset.variablesQuantity) + "\n");
  datasetFile.write(dataset.variablesCardinality + "\n");
  datasetFile.write(str(len(dataset.data)) + "\n");
  for dataLine in dataset.data:
   datasetFile.write(dataLine);
 return datasetFileName;

def ScoreDatasetFile(pathToScorer, pathToDataset, alpha, palim):
 scoreFileName = os.path.splitext(pathToDataset)[0] + ".score";
 scoreCommand = [pathToScorer, pathToDataset, str(alpha), str(palim)]
 with open(scoreFileName, "w") as scoreFile:
  call(scoreCommand, stdout = scoreFile, shell = False);
 return scoreFileName;

def LearnWithGobnilp(pathToGobnilp, pathToScore):
 resultFilename = os.path.splitext(pathToScore)[0] + ".gobnilp.result";
 timeFilename = os.path.splitext(pathToScore)[0] + ".gobnilp.time";

 with open("gobnilp.set", "w") as gobnilpSettings:
  gobnilpSettings.write("gobnilp/outputfile/solution = \"" + resultFilename + "\"\n");
  gobnilpSettings.write("gobnilp/outputfile/scoreandtime = \"" + timeFilename + "\"\n");

 gobnilpCommand = [pathToGobnilp, pathToScore]
 call(gobnilpCommand, shell = False);

 return resultFilename, timeFilename;

def LearnWithTwilp(pathToTwilp, pathToScore, treewidth):
 resultYFilename = os.path.splitext(pathToScore)[0] + ".twilp.y_result.gml";
 resultZFilename = os.path.splitext(pathToScore)[0] + ".twilp.z_result.gml";
 timeFilename = os.path.splitext(pathToScore)[0] + ".twilp.time";
 twilpCommand = ["python", pathToTwilp, "-t="+str(treewidth), "-f="+pathToScore];
 call(twilpCommand, shell=False);

 twilpBaseName = "tw_"+str(treewidth)+"_mp_0_"+os.path.basename(pathToScore);
 call(["rm", "-rf", twilpBaseName + ".lp"], shell=False);
 call(["rm", "-rf", twilpBaseName + "_gap_scores.csv"], shell=False);
 call(["mv", twilpBaseName+".result", timeFilename], shell=False);
 call(["mv", twilpBaseName+"_y.gml", resultYFilename], shell=False);
 call(["mv", twilpBaseName+"_z.gml", resultZFilename], shell=False); 
 return resultYFilename, resultZFilename, timeFilename;

def main():
#CONFIG VARIABLES
 # PATHS
 pathToGobnilp = "/opt/bnet/learning/gobnilp-1.4.1-cplex/bin/gobnilp";
 pathToTwilp = "/opt/bnet/learning/twilp/twilp.py";
 pathToScorer = "/opt/bnet/learning/gobnilp-1.4.1-cplex/scoring"; 
 pathToDataset = "files/nursery_bin.data";
 pathTosubdatasets = "parsedFiles";

 # PARAMETERS
 folds = 10;                     # Number of cross validation "folds" to be created for each dataset
 alpha = 1;                      # Alpha parameter for scorer;
 palim = 4;                      # Limit of variables' fathers (used by scorer);
 treewidth = 3;
##
 
 dataset = ParseFile(pathToDataset);
 datasetPath = CreateDatasetDirectory(pathTosubdatasets, dataset);
 for training, validation in KFoldCrossValidation(dataset, folds):
  WriteDatasetToFile(datasetPath, validation);
  trainingFileName = WriteDatasetToFile(datasetPath, training);
  scoreFileName = ScoreDatasetFile(pathToScorer, trainingFileName, alpha, palim);
  gobnilpResult = LearnWithGobnilp(pathToGobnilp, scoreFileName);
  twilpResult = LearnWithTwilp(pathToTwilp, scoreFileName, treewidth);

if __name__ == "__main__":
 main();

    # TODO:
    # OK: Create dataset class
    # OK: Parse file and create a dataset object
    # OK: Cross validate the dataset into subdatasets
    # OK: Creat subdirectory structure
    # OK: Save the subdataset to files
    # OK: Run scoring in each training dataset
    # OK: Run gobnilp foreach score file
    # Run twilp for each score file
    # Create BNTree class
    # Parser gobnilp result and create a BNTree instance
    # Parser twilp result and create another BNTree instance
    # Apply MLE in the test instances of datasets with the Gobnilp BNTree
    # Apply MLE in the test instances of datasets with the Twilp BNTree
