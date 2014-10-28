#!/bin/python
# Read a dataset file, a twilp gml graphadjacency matrix file and print the likelihood of the dataset.

import sys
import numpy
import networkx
from subprocess import call
from Dataset import Dataset
from data_likelihood import compute_likelihood

def GetGraphFromTwilpFile(twilpResult):
 return networkx.read_gml(twilpResult);

def GetListOfParents(twilpResult):
 twilpGraph = GetGraphFromTwilpFile(twilpResult);
 return [twilpGraph.predecessors(node) for node in twilpGraph.nodes()];

def Main(datasetFile, graphFile, ess):
 dataset = Dataset();
 dataset.ParseFile(datasetFile);
 return compute_likelihood(dataset.data, dataset.variablesCardinality, GetListOfParents(graphFile), ess);

def Error():
 print "Usage:", sys.argv[0], "data_filename", "graph_file", "ess";
 exit(0); 

if __name__ == "__main__":
 if len(sys.argv) < 4:
  Error();

 print "Likelihood:", Main(sys.argv[1], sys.argv[2], float(sys.argv[3]));
