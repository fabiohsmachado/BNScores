#!/bin/python
# Read a list of score files from the Gobnilp's scorer and learn the BN structure using Gobnilp.
import sys
import os
from subprocess import call

def LearnWithTwilp(pathToTwilp, pathToScore, treewidth):
 print "Learning the network structures from file", pathToScore, "using Twilp and treewidth", treewidth;
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
 print "Finished learning.";
 return resultYFilename, resultZFilename, timeFilename;

def LearnTwilpVariable(fileList, variablesQuantity):
 pathToTwilp = "/opt/bnet/learning/twilp/twilp.py";

 treewidths = [3, 4, 5];
 treewidth = 10;
 while(treewidth <= variablesQuantity / 2):
  treewidths.append(treewidth);
  treewidth += 5;

 results = [[LearnWithTwilp(pathToTwilp, datasetFile, tw) for datasetFile in fileList if os.path.isfile(datasetFile)] for tw in treewidths];
 YresultFiles, ZresultFiles, timeFiles = [[[t[s][f] for t in results] for s in xrange(len(results[0]))] for f in xrange(len(results[0][0]))];
 return treewidths, YresultFiles, ZresultFiles, timeFiles;
 
def LearnTwilp(fileList, treewidth):
 pathToTwilp = "/opt/bnet/learning/twilp/twilp.py";
 results =  [LearnWithTwilp(pathToTwilp, datasetFile, treewidth) for datasetFile in fileList if os.path.isfile(datasetFile)];
 YresultFiles, ZresultFiles, timeFiles = [[row[i] for row in results] for i in range(len(results[0]))];
 return YresultFiles, ZresultFiles, timeFiles;

def Error():
 print "Usage:", sys.argv[0], "data_files treewidth";
 exit(0);

if __name__ == "__main__":
 try:
  LearnTwilpVariable(sys.argv[1:], int(sys.argv[-1]));
 except:
  Error();
