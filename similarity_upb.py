#!/bin/python

from utils import *
import sys
from compare_locations import compare_locations


# json_file = "25-02-2021_21-16-46.json"
json_file_1 = sys.argv[1]
json_file_2 = sys.argv[2]


# preprocessing(json_file)

# Load all collections from data file
collections1 = load_dataset_json(json_file_1)
print("len=", len(collections1))
collections2 = load_dataset_json(json_file_2)


# Get all RSSI
# rss_v = get_rssi_from_collections(json_file, collections)





# print("Locations whitin range: ", similarity_collection_vs_all(json_file, collections,
#             index = 5, method = 'First', label = "First RSSI value"))

# printf("Select random RSSI values from each AP")
# for i in range(1,15):
#     print("Locations within range: ", similarity_collection_vs_all(json_file, collections,
#             index = 5, method = 'Random'+str(i), label = "Random "+str(i)+" RSSI from each AP"))
# 

#print("Locations whitin range: ", similarity_collection_vs_all(json_file_1, collections1,
#             index = 5, method = 'Average'))


print(get_rssi_from_collections(collections1))

# 
# print("Locations whitin range: ", similarity_collection_vs_all(json_file, collections,
#             index = 5, method = 'Tempered'))

# print("Locations whitin range: ", similarity_collection_vs_all(json_file, collections,
#               index = 5, method = 'Chi-squared'))


# print("Locations whitin range: ", similarity_collection_vs_all(json_file, collections,
#               index = 5, method = 'Histogram'))



# similarity_collection_vs_all(json_file, collections, index = 5, method = 'Median')
# similarity_collection_vs_all(json_file, collections, index = 5, method = 'Histogram')

# 
# print(get_rssi_from_collections(json_file,collections))

#print(compare_locations(collections1[3], collections2[4]))





