#!/bin/python
# Read a list of score files from the Gobnilp's scorer and learn the BN structure using Gobnilp.
import sys
import os
from subprocess import call

def LearnWithGobnilp(pathToGobnilp, pathToScore):
 print "Learning the network structures from file", pathToScore, "using Gobnilp."
 baseName = os.path.splitext(pathToScore)[0];
 resultFilename = baseName + ".gobnilp.result";
 timeFilename = baseName + ".gobnilp.time";
 matrixFilename = baseName + ".gobnilp.matrix";

 with open("gobnilp.set", "w") as gobnilpSettings:
  gobnilpSettings.write("gobnilp/outputfile/solution = \"" + resultFilename + "\"\n");
  gobnilpSettings.write("gobnilp/outputfile/scoreandtime = \"" + timeFilename + "\"\n");
  gobnilpSettings.write("gobnilp/outputfile/adjacencymatrix = \"" + matrixFilename + "\"\n");

 gobnilpCommand = [pathToGobnilp, "-f=jkl", pathToScore];
 call(gobnilpCommand, shell = False, stdout=open(os.devnull, "w"));
 call(["rm", "-f", "gobnilp.set"], shell=False);
 print "Finished learning."
 return matrixFilename, resultFilename, timeFilename;

def Error():
 print "Usage:", sys.argv[0], "data_filenames";
 exit(0);

def LearnGobnilp(fileList):
 pathToGobnilp = "/opt/bnet/learning/gobnilp-1.4.1-cplex/bin/gobnilp";
 results =  [LearnWithGobnilp(pathToGobnilp, datasetFile) for datasetFile in fileList if os.path.isfile(datasetFile)];
 matrixFiles, resultFiles, timeFiles = [[row[i] for row in results] for i in range(len(results[0]))];
 return matrixFiles, resultFiles, timeFiles;

if __name__ == "__main__":
 try:
  LearnGobnilp(sys.argv[1:]);
 except:
  Error();

