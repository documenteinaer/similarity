#!/bin/python
import sys
from server_utils import *
from preprocessing import *

# Preprocessing Phase; it will result a file "p_json_name"
preprocessing(sys.argv[1])
input_json = "p_"+sys.argv[1]

# Load collections from preprocessed files
collections = load_collections(input_json)

# Compare two locations
similarity = compare_locations(collections[3], collections[4])
print("Similarity :", similarity)
