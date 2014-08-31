#!/bin/python
# Read a list of score files from the Gobnilp's scorer and learn the BN structure using Gobnilp.
import sys
import os
from subprocess import call

def LearnWithTwilp(pathToTwilp, pathToScore, treewidth):
 print "Learning the network structures from file", pathToScore, "using Twilp."
 resultYFilename = os.path.splitext(pathToScore)[0] + ".twilp."+str(treewidth)+".y_result.gml";
 resultZFilename = os.path.splitext(pathToScore)[0] + ".twilp."+str(treewidth)+".z_result.gml";
 timeFilename = os.path.splitext(pathToScore)[0] + ".twilp."+str(treewidth)+".time";
 twilpCommand = ["python", pathToTwilp, "-t="+str(treewidth), "-f="+pathToScore];
 call(twilpCommand, shell=False, stdout=open(os.devnull, "w"));

 twilpBaseName = "tw_"+str(treewidth)+"_mp_0_"+os.path.basename(pathToScore);
 call(["rm", "-f", twilpBaseName + ".lp"], shell=False);
 call(["rm", "-f", twilpBaseName + "_gap_scores.csv"], shell=False);
 call(["mv", twilpBaseName+".result", timeFilename], shell=False);
 call(["mv", twilpBaseName+"_y.gml", resultYFilename], shell=False);
 call(["mv", twilpBaseName+"_z.gml", resultZFilename], shell=False);
 print "Finished learning the network structures from file", pathToScore, "using Gobnilp."
 return resultYFilename, resultZFilename, timeFilename;

def Error():
 print "Usage:", sys.argv[0], "data_files, treewidth.";
 exit(0);

def Main(argList):
 pathToTwilp = "/opt/bnet/learning/twilp/twilp.py";

 for datasetFile in argList[:-1]:
  if os.path.isfile(datasetFile):
   LearnWithTwilp(pathToTwilp, datasetFile, int(argList[-1]));

if __name__ == "__main__":
 if len(sys.argv) < 4:
  Error();

 Main(sys.argv[1:]);
