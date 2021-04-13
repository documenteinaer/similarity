#!/bin/python
import sys
from server_utils import *
from preprocessing import *
import matplotlib.pyplot as plt


# Preprocessing Phase; it will result a file "p_json_name"
preprocessing(sys.argv[1])
input_json = "p_"+sys.argv[1]

# Load collections from preprocessed files
collections = load_collections(input_json)

# Compare two locations
similarity = compare_locations(collections[3], collections[4])
print("Similarity :", similarity)




############## Plotting purposes only ###################

similarity_array = []
for c in range(len(collections)):
    similarity_array.append(compare_locations(collections[3], collections[c]))

plt.plot(similarity_array, 'o', label = "Similarity (Average)")
plt.xlabel("Nr. crt.")
plt.ylabel("Similarity Measurement")
plt.legend()
plt.show()


