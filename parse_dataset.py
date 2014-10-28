#!/bin/python
import sys
import os
import numpy
import networkx
from Dataset import Dataset
from subprocess import call

def getGraphFromGobnilpFile(gobnilpResult):
 matrix = "";
 with open(gobnilpResult, "r") as gobnilpResultFile:
  for line in gobnilpResultFile:
   print line;
   matrix += line.strip('\n') + "; "
  matrix = matrix[:-2];
 return networkx.from_numpy_matrix(numpy.matrix(matrix), create_using=networkx.MultiDiGraph());

def getGraphFromTwilpFile(twilpResult):
 return networkx.read_gml(twilpResult);

def main():
 datasetFiles = os.listdir(pathToDatasets);
 datasetFiles.sort();
 for datasetFile in datasetFiles:
  dataset = Dataset();
  print "Started processing the " + datasetFile + " dataset:"
  dataset.ParseFile(pathToDatasets + "/" + datasetFile);
  datasetPath = CreateDatasetDirectory(pathTosubdatasets, dataset);
  
  print " Started processing score files.";
  trainingFiles = [];
  validationFiles = [];
  for training, validation in dataset.KFoldGenerator(folds):
   validationFileName = validation.WriteToFile(datasetPath);
   trainingFileName = training.WriteToFile(datasetPath);
   trainingFiles.append(trainingFileName);
   validationFiles.append(validationFileName);
  
  # scoreFiles = [];
  # for trainingFile in trainingFiles:
  #  scoreFileName = ScoreDatasetFile(pathToScorer, trainingFile, alpha, palim);
  #  scoreFiles.append(scoreFileName);
  # print " Finished processing score files.";

  # print " Started learning the structures files.";
  # gobnilpResults = [];
  # twilpResults = [];
  # twilpTreewidthResults = [];
  # for scoreFile in scoreFiles:
  #  print " Score file " + scoreFile + ":";
  #  gobnilpResult = LearnWithGobnilp(pathToGobnilp, scoreFile);
  #  gobnilpResults.append(gobnilpResult);
  #  print "  Gobnilp finished";

  #  treewidth = 3
  #  twilpResult = LearnWithTwilp(pathToTwilp, scoreFile, treewidth);
  #  twilpTreewidthResults.append(twilpResult);
  #  print " Twilp, treewidth " + str(treewidth) + " finished.";

  #  treewidth = 4;
  #  twilpResult = LearnWithTwilp(pathToTwilp, scoreFile, treewidth);
  #  twilpTreewidthResults.append(twilpResult);
  #  print " Twilp, treewidth " + str(treewidth) + " finished.";

  #  treewidth = 5;
  #  while(treewidth <= dataset.variablesQuantity / 2):
  #   twilpResult = LearnWithTwilp(pathToTwilp, scoreFile, treewidth);
  #   twilpTreewidthResults.append(twilpResult);
  #   print " Twilp, treewidth " + str(treewidth) + " finished.";
  #   treewidth += 5;
  #  twilpResults.append(twilpTreewidthResults);
  # print "Finished processing the " + datasetFile + " dataset.\n"

 # gobnilpResults = [];
 # gobnilpResult = "parsedFiles/nursery_bin/nursery_bin.0.training.gobnilp.matrix";
 # gobnilpResults.append(gobnilpResult);
 # for gobnilpResult in gobnilpResults:
 #   gobnilpGraph = getGraphFromGobnilpFile(gobnilpResult);

 #   print gobnilpGraph.edges();
 #   print gobnilpGraph.nodes();
 #   for node in gobnilpGraph.nodes():
 #    print str(node) + ": ";
 #    print gobnilpGraph.predecessors(node);


 # twilpResults = [];
 # twilpTreewidthResults = [];
 # twilpTreewidthResult = "parsedFiles/nursery_bin/nursery_bin.0.training.twilp.3.z_result.gml";
 # twilpTreewidthResults.append(twilpTreewidthResult);
 # twilpResults.append(twilpTreewidthResults);
 # for twilpResult in twilpResults:
 #  for twilpTreewidthResult in twilpTreewidthResults:
 #   twilpGraph = getGraphFromTwilpFile(twilpTreewidthResult);

 #   print twilpGraph.nodes();
 #   print twilpGraph.edges();

if __name__ == "__main__":
 main();

    # TODO:
    # OK: Parse gobnilp result and create a BNTree instance
    # OK: Parse twilp result and create another BNTree instance
    # Apply MLE in the test instances of datasets with the Gobnilp BNTree
    # Apply MLE in the test instances of datasets with the Twilp BNTree
