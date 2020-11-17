#!/bin/python

import csv
import sys
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine
from scipy.spatial.distance import cityblock
from scipy.spatial.distance import minkowski
from scipy.spatial.distance import jaccard
from sklearn import preprocessing



loc1 = int(sys.argv[1])
loc2 = int(sys.argv[2])
locations = []

def load_dataset():
    dev = []
    d = []
    x_y_z = []
    rss = []

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
        location_tuple = (dev[i], d[i], x_y_z[i], rss[i])
        locations.append(location_tuple)

def norm_rss():
    for loc in locations:
        for rss in range(len(loc[3])):
            # Negative RSS turn to positive
            if loc[3][rss] < 0:
                loc[3][rss] = -loc[3][rss]

            # If not found, make 10.000
            if loc[3][rss] == 100:
                loc[3][rss] = 40


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

def get_nearest_locations(location, meters = 20):
    nearest = []
    for l in locations:
        if physical_distance(location, l) < meters:
            nearest.append(l)

    return nearest

# AP positions
def plot_similarities(location):
    physical_plot = []
    cosine_plot = []
    cityblock_plot = []
    euclidean_plot = []
    minkowski_plot = []
    jaccard_plot = []

    for l in get_nearest_locations(location):
        if physical_distance(l, location) == 0:
            continue
        physical_plot.append(physical_distance(l, location))
        cosine_plot.append(cosine(tuple(l[3]), tuple(location[3])))
        cityblock_plot.append(cityblock(tuple(l[3]), tuple(location[3])))
        euclidean_plot.append(euclidean(tuple(l[3]), tuple(location[3])))
        minkowski_plot.append(minkowski(tuple(l[3]), tuple(location[3]), 3))
        jaccard_plot.append(jaccard(tuple(l[3]), tuple(location[3])))


    # Sort plotting arrays
    #physical_plot = sorted(physical_plot, key=float)
    #cosine_plot = sorted(cosine_plot, key=float)
    #cityblock_plot = sorted(cityblock_plot, key=float)
    #euclidean_plot = sorted(euclidean_plot, key=float)
    #minkowski_plot = sorted(minkowski_plot, key=float)
    #jaccard_plot = sorted(jaccard_plot, key=float)

    # Plot similarities. Attention to the scale
    plt.plot(physical_plot, cityblock_plot, 'o', label = "line 1")
    #plt.plot(physical_plot, euclidean_plot, 'o', label = "line 1")
    #plt.plot(physical_plot, minkowski_plot, 'o', label = "line 1")
    #plt.plot(physical_plot, cosine_plot, 'o', label = "line 1")
    #plt.plot(physical_plot, jaccard_plot, 'o', label = "line 1")

    # Standardization
    #plt.plot(physical_plot, preprocessing.scale(cityblock_plot), 'o', label = "line 1")
    #plt.plot(physical_plot, preprocessing.scale(euclidean_plot), 'o', label = "line 2")
    #plt.plot(physical_plot, preprocessing.scale(minkowski_plot), 'o', label = "line 3")
    #plt.plot(physical_plot, preprocessing.scale(cosine_plot), 'o', label = "line 4")
    #plt.plot(physical_plot, preprocessing.scale(jaccard_plot), 'o', label = "line 5")



    plt.legend()
    plt.show()


load_dataset()
norm_rss()

print("Coordinates:")
print(locations[loc1][2])
print(locations[loc2][2])
print("The (X,Y,Z) Euclidian distance:")
print(physical_distance(locations[loc1], locations[loc2]))
print("Similarity distances:")
print(similarity(locations[loc1], locations[loc2], cosine))
print(similarity(locations[loc1], locations[loc2], cityblock))
print(similarity(locations[loc1], locations[loc2], euclidean))
print(similarity(locations[loc1], locations[loc2], minkowski, 50))
print(similarity(locations[loc1], locations[loc2], jaccard))
#similarity(locations[loc1], locations[loc2])
plot_similarities(locations[loc1])
