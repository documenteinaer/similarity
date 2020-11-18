import csv
import sys
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine
from scipy.spatial.distance import cityblock
from scipy.spatial.distance import minkowski
from scipy.spatial.distance import jaccard
from sklearn import preprocessing
import scipy.sparse as sp
from collections import Counter



def load_dataset():
    dev = []
    d = []
    x_y_z = []
    rss = []
    avail_rss = []
    locations = []

    # Load Devices
    with open('../datasets/DISTRIBUTED_OPENSOURCE_version2/FINGERPRINTING_DB/Test_device_21Aug17.csv') as devices_csv:
        devices = csv.reader(devices_csv, delimiter=',')
        for i in devices:
            dev.append(i[0])

    # Load Dates
    with open('../datasets/DISTRIBUTED_OPENSOURCE_version2/FINGERPRINTING_DB/Test_date_21Aug17.csv') as dates_csv:
        dates = csv.reader(dates_csv, delimiter=',')
        for i in dates:
            d.append(i[0])

    # Load Coordinates
    with open('../datasets/DISTRIBUTED_OPENSOURCE_version2/FINGERPRINTING_DB/Test_coordinates_21Aug17.csv') as coord_csv:
        coord = csv.reader(coord_csv, delimiter=',')
        for i in coord:
            xyz = [float(numeric_string) for numeric_string in i]
            x_y_z.append(xyz)

    # Load RSS
    with open('../datasets/DISTRIBUTED_OPENSOURCE_version2/FINGERPRINTING_DB/Test_rss_21Aug17.csv') as rss_csv:
        rssi = csv.reader(rss_csv, delimiter=',')
        for i in rssi:
            rsss = [int(numeric_string) for numeric_string in i]
            rss.append(rsss)

    # locations = (device, date, [x,y,z], [AP1, AP2, ..])
    for i in range(0,len(dev)):
        avail_rss = len(rss[i]) - Counter(rss[i])[100]
        location_tuple = (dev[i], d[i], x_y_z[i], rss[i], avail_rss)
        locations.append(location_tuple)

    return locations

def norm_rss(locations):
    for loc in locations:
        for rss in range(len(loc[3])):
            # Negative RSS turn to positive
            if loc[3][rss] < 0:
                loc[3][rss] = -loc[3][rss]

            # If not found, make 10.000
            if loc[3][rss] == 100:
                loc[3][rss] = 100
    return locations

# X Y Z positions
def physical_distance(location1, location2):
    return euclidean(tuple(location1[2]), tuple(location2[2]))

# AP positions
def similarity(location1, location2, method = None, minkowski_p=10):

    if not method:
        print("Cosine Distance:")
        print(cosine(tuple(location1[3]), tuple(location2[3])))
        print("Manhattan Distance:")
        print(cityblock(tuple(location1[3]), tuple(location2[3])))
        print("Euclidean Distance:")
        print(euclidean(tuple(location1[3]), tuple(location2[3])))
        print("Minkowski Distance:")
        print(minkowski(tuple(location1[3]), tuple(location2[3]), 50))
        print("Jaccard Similarity:")
        print(jaccard(tuple(location1[3]), tuple(location2[3])))
    elif method.__name__ == "minkowski":
        return method(tuple(location1[3]), tuple(location2[3]), minkowski_p)
    else:
        return method(tuple(location1[3]), tuple(location2[3]))

def get_nearest_locations(location, locations, meters = 20):
    nearest = []
    for l in locations:
        if physical_distance(location, l) < meters:
            nearest.append(l)

    return nearest

def get_common_APs(loc1, loc2):
    count_b = 0
    count_1 = 0
    count_2 = 0
    for i in range(len(loc1[3])):
        if loc1[3][i] != 100 and loc2[3][i] != 100:
            count_b += 1
        if loc1[3][i] == 100 and loc2[3][i] != 100:
            count_2 += 1
        if loc1[3][i] != 100 and loc2[3][i] == 100:
            count_1 += 1

    return [count_1, count_2, count_b]
