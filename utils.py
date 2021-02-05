import csv
import sys
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine
from scipy.spatial.distance import cityblock
from scipy.spatial.distance import minkowski
from scipy.spatial.distance import jaccard
from scipy.spatial.distance import braycurtis
from sklearn import preprocessing
import scipy.sparse as sp
from collections import Counter
import datetime
import math
import json
import numpy as np


min_rssi = -100


def get_all_APs_in_json(json_file):
    APs = []
    f = open(json_file)
    data = json.load(f)

    coll_no = 0
    while 'collection'+str(coll_no) in data:
        collection = data['collection'+str(coll_no)]
        fingerprints = collection['fingerprints']

        # Remove empty fingerprints (Location not Activated)
        if not fingerprints:
            coll_no += 1
            continue

        rsss = []
        for f in fingerprints:
            wifi = f['wifi']
            for ap in wifi.keys():
                APs.append(ap)

        coll_no += 1

    return APs

def load_dataset_json(json_file):
    collections = []
    fingerprints = []
    coll_no = 0

    f = open(str(json_file))
    data = json.load(f)

    while 'collection'+str(coll_no) in data:
#         print('collection'+str(coll_no))
        fingerprint = data['collection'+str(coll_no)]['fingerprints']
#         print(data['collection'+str(coll_no)]['devName'])

        # Remove empty fingerprints (Location not Activated)
        if not data['collection'+str(coll_no)]['fingerprints']:
            coll_no += 1
            continue

        collections.append(data['collection'+str(coll_no)])
        fingerprints.append(fingerprint)

#         rsss = []
#         for f in fingerprints:
#             wifi = f['wifi']
#             print(f['timestamp'])
#             for ap in wifi.keys():
#                 print(ap)
#                 print(wifi[ap]['rssi'])


        # No WiFi detected
#         if not wifi:
#             coll_no += 1
#             continue
#
#         print(wifi)

        # Go to next collection
        coll_no += 1

    return collections

def get_wifi_from_collections(json_file, collections):
    rss_v= []

    APs = get_all_APs_in_json(json_file)
    for c in collections:
        rss = {}
        for ap in APs:
            rss[ap] = []
            for f in c['fingerprints']:
                if not ap in  f['wifi']:
                    continue
#                 rss[ap].append(f['wifi'][ap]['ssid'])
#                 print(ap+" "+f['wifi'][ap]['ssid']+" "+f['wifi'][ap]['rssi'])
                rss[ap].append(int(f['wifi'][ap]['rssi']))
#                 wifi[ap].append(
#             print(c['devName']+" "+ap+" "+str(rss[ap]))
        rss_v.append(rss)
    return rss_v


def similarity_collection_vs_all(json_file, collections, index = 0, method = 'First'):
    rss_v = get_wifi_from_collections(json_file, collections)
    sorensen_plot = []

    for r in range(len(rss_v)):
        print("###########")
        print("Collection " + str(index) + " rss: " + str(rss_v[index]))
        print("Collection "+ str(r) + " rss: " + str(rss_v[r]))
        print("###########")
        rss_1 = []
        rss_2 = []
        for key in rss_v[index].keys():

            # Both collections should see the AP;
            if not rss_v[index][key] or not rss_v[r][key]:
                continue

            # Take only the first value
            if method == 'First':
                rss_1.append(rss_v[index][key][0])
                rss_2.append(rss_v[r][key][0])

            if method == 'Average':
                rss_1.append(np.average(rss_v[index][key]))
                rss_2.append(np.average(rss_v[r][key]))


        sorensen_plot.append(braycurtis(tuple(rss_1), tuple(rss_2)))

    plt.plot(sorensen_plot, 'o', label = "Sorensen")
    plt.xlabel("Nr. crt.")
    plt.ylabel("Similarity Measurement")
    plt.legend()
    plt.show()


def load_dataset_uji():
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

    # locations = (device, date, [x,y,z], [AP1, AP2, ..], avail_APs)
    for i in range(0,len(dev)):
        avail_rss = len(rss[i]) - Counter(rss[i])[100]
        location_tuple = (dev[i], d[i], x_y_z[i], rss[i], avail_rss)
        locations.append(location_tuple)

    return locations

def norm_rss(locations):
    for loc in locations:
        for rss in range(len(loc[3])):
            # Negative RSS turn to positive
            if loc[3][rss] < 0 and loc[3][rss] > -91:
                # Linear values
#                 loc[3][rss] = loc[3][rss] - min_rssi
                # Exponential values
                positive = loc[3][rss] - min_rssi
                loc[3][rss] = pow(positive, math.e)/pow(-min_rssi, math.e)

            else:
                loc[3][rss] = 0

            # If not found, make 10.000
            if loc[3][rss] == 100:
                loc[3][rss] = 0
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

def select_locations(location, locations, meters, same_device = False,
                     same_floor = False, same_month = False):
    selection = []
    for l in locations:

        # Remove the exact location (first parameter)
        if physical_distance(l, location) == 0:
            continue

        # If same_device is set, check if devices are the same
        if same_device and (l[0] != location[0]):
            continue
        # If same_floor is set, check if floors are the same
        if same_floor and (l[2][2] != location[2][2]):
            continue

        # If same_month is set, check if months are the same
        if same_month and \
            (datetime.datetime.strptime(l[1], "%Y-%m-%d %H:%M:%S").month !=
             datetime.datetime.strptime(location[1], "%Y-%m-%d %H:%M:%S").month):
            continue

        # Check if 
        if meters and (physical_distance(location, l) > meters):
            continue

        selection.append(l)

    return selection

def get_number_APs(loc1, loc2):
    count_b = 0
    count_1 = 0
    count_2 = 0
    for i in range(len(loc1[3])):
        if loc1[3][i] != 100 and loc2[3][i] != 100:
            #print(str(loc1[3][i])+", "+str(loc2[3][i]))
            count_b += 1
            #print(str(loc1[3][i])+", "+str(loc2[3][i]))
        if loc2[3][i] != 100:
            count_2 += 1
            #print(str(loc1[3][i])+", "+str(loc2[3][i]))
        if loc1[3][i] != 100:
            count_1 += 1

    #print(str(count_1)+", "+str(count_2)+", "+str(count_b))
    return [count_1, count_2, count_b]

def get_common_APs(loc1, loc2):
    APs_in_1 = []
    APs_in_2 = []

    for i in range(len(loc1[3])):
        if loc1[3][i] != 0 and loc2[3][i] != 0:
            APs_in_1.append(loc1[3][i])
            APs_in_2.append(loc2[3][i])

    return [APs_in_1, APs_in_2]
