#!/bin/bash

# Check if the user provided the correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <dataset_name>"
    exit 1
fi

# Parse arguments
dataset_name="$1"

# Construct paths
dataset_folder="data/$dataset_name"

# Validate dataset folder existence
if [ ! -d "$dataset_folder" ]; then
    echo "Error: Dataset folder '$dataset_folder' does not exist."
    exit 2
fi

# Run the Python script
python remove_artifact.py -d "$dataset_folder"
