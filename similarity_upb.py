#!/bin/python

from utils import *
import sys

# json_file = "25-02-2021_21-16-46.json"
json_file = sys.argv[1]
# Load all collections from data file
collections = load_dataset_json(json_file)

# Get all RSSI
# rss_v = get_rssi_from_collections(json_file, collections)



preprocessing(json_file)


similarity_collection_vs_all(json_file, collections, index = 5, method = 'First')
print("Locations whitin range: ", similarity_collection_vs_all(json_file, collections, index = 5, method = 'Average'))
# similarity_collection_vs_all(json_file, collections, index = 5, method = 'Median')
# similarity_collection_vs_all(json_file, collections, index = 5, method = 'Histogram')

# 
# print(get_rssi_from_collections(json_file,collections))

