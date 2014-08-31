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

 gobnilpCommand = [pathToGobnilp, pathToScore];
 call(gobnilpCommand, shell = False, stdout=open(os.devnull, "w"));
 call(["rm", "-f", "gobnilp.set"], shell=False);
 print "Finished learning the network structures from file", pathToScore, "using Gobnilp."
 return matrixFilename, resultFilename, timeFilename;

def Error():
 print "Usage:", sys.argv[0], "data_filename", "number_of_folds";
 exit(0);

def Main(argList):
 pathToGobnilp = "/opt/bnet/learning/gobnilp-1.4.1-cplex/bin/gobnilp";
 for scoreFile in argList:
  if os.path.isfile(scoreFile):
   LearnWithGobnilp(pathToGobnilp, scoreFile);

if __name__ == "__main__":
 if len(sys.argv) < 3:
  Error();

 Main(sys.argv[1:]);
