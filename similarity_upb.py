#!/bin/python

from utils import *
json_file = "upb1.json"
# Load all collections from data file
collections = load_dataset_json(json_file)

# Get all RSSI
# rss_v = get_rssi_from_collections(json_file, collections)

""" Plot similarity (only Sorensen used). Params:
    * index - the index in the collection array. All collection are compared with it
    * method - the method used for rssi value. Examples:
        * 'First'
        * 'Average'
"""
similarity_collection_vs_all(json_file, collections, index = 0, method = 'First')
similarity_collection_vs_all(json_file, collections, index = 0, method = 'Average')
