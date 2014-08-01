class Dataset:
 def __init__(self):
  self.data = [];
  self.variablesQuantity = 0;
  self.variablesCardinality = [];

def ParseFile(filename):
 dataset = Dataset();
 with open(filename, "r") as datasetFile:
  dataset.variablesQuantity = int(datasetFile.readline());
  dataset.variablesCardinality = datasetFile.readline().strip('\n');
  datasetFile.readline();
  for line in datasetFile:
   dataset.data.append(line);
  return dataset;

def main():
 dataset = ParseFile("files/nursery_bin.data");
 print dataset.variablesQuantity;
 print dataset.variablesCardinality;
 print dataset.data;

    # TODO:
    # OK: Create dataset class
    # OK: Parse file and create a dataset object
    # Cross validate the dataset into subdatasets
    # Creat subdirectory structure
    # Save the subdataset to files
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
