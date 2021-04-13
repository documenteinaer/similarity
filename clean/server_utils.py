import json
import numpy as np
from scipy.spatial.distance import braycurtis


# Loads collections from json_file
def load_collections(json_file):
    collections = []

    f = open(json_file, 'r')
    data = json.load(f)

    for col in data.keys():
        # Remove empty fingerprints (Location not Activated)
        if not data[col]['fingerprints']:
            continue

        collections.append(data[col])

    return collections


#  Given two locations (collections) it performs a Sorensen similarity.
def compare_locations(c1, c2, method = 'Average'):
    rssi1 = []
    rssi2 = []
    wifi1 = c1['fingerprints']['wifi']
    wifi2 = c2['fingerprints']['wifi']

    common_aps = list(set(wifi1.keys()) & set(wifi2.keys()))

    # No APs in common -> similarity = 1
    if not common_aps:
        return 1

    # TODO: find the best metric
    # If not enough common APs -> similarity = 1
    if len(common_aps) * 10 < len(wifi1.keys()):
        return 1

    for ap in common_aps:
        # Take only the first RSSI value
        if method == 'First':
            rssi1.append(wifi1[ap]['rssi'][0])
            rssi2.append(wifi2[ap]['rssi'][0])

        # Make an average of all RSSI values
        if method == 'Average':
            rssi1.append(np.average(wifi1[ap]['rssi']))
            rssi2.append(np.average(wifi2[ap]['rssi']))

    return braycurtis(tuple(rssi1), tuple(rssi2))
