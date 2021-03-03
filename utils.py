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

"""
Takes the original json file and creates a new json file with the fingerprints array merged
into a single json element.
"""


def preprocessing(json_file):

    f = open(json_file)
    data = json.load(f)
    collections = {}

#     while 'collection'+str(coll_no) in data:
    for c in data.keys():
        collection = data[c]

        # Transform array of fingerprints into a single fingerprint
        fingerprints = collection['fingerprints']
        if not fingerprints:
            continue
        fingerprint = fingerprints[0]

        for f in fingerprints:
            for mac in f["wifi"].keys():
                if not mac in fingerprint["wifi"]:
                    fingerprint["wifi"][mac] = f["wifi"][mac]
                # TODO: Check if 2 MAC address are from the same WiFi
            for mac in f["ble"].keys():
                if not mac in fingerprint["ble"]:
                    fingerprint["ble"][mac] = f["ble"][mac]




        collection["fingerprints"] = fingerprint
        collections[c] = collection

    with open('json2.json', 'w') as outfile:
        json.dump(collections, outfile, indent = 4)



def get_all_APs_in_json(json_file, whitelist = False):
    APs = []
    f = open(json_file)
    data = json.load(f)
    w = open('whitelist.txt', 'r')
    whitelist_ap = w.read().splitlines()
    print("#######",whitelist_ap)

    coll_no = 0
    while 'collection'+str(coll_no) in data:
        collection = data['collection'+str(coll_no)]
        fingerprints = collection['fingerprints']

        # Remove empty fingerprints (Location not Activated)
        if not fingerprints:
            coll_no += 1
            continue

        # For every fingerprint
        wifi = fingerprints['wifi']

        # For every MAC address
        for ap in wifi.keys():
            if not whitelist:
                APs.append(ap)
            # WHITELIST
            elif str(ap) in whitelist_ap:
                APs.append(ap)

        coll_no += 1

    return APs

def load_dataset_json(json_file):
    collections = []
    fingerprints = []
    coll_no = 0

    f = open(str(json_file))
    data = json.load(f)

    for col in data.keys():
        fingerprint = data[col]['fingerprints']
#         print(data['collection'+str(coll_no)]['devName'])

        # Remove empty fingerprints (Location not Activated)
        if not data[col]['fingerprints']:
            continue

        collections.append(data[col])
        fingerprints.append(fingerprint)


    return collections

def get_rssi_from_collections(json_file, collections):
    rssi_v= []

    APs = get_all_APs_in_json(json_file)

    for c in collections:

        rss = {}
        for ap in APs:
            rss[ap] = []
            for f in c['fingerprints']:
                if not ap in f['wifi']:
                    continue
                rssi = int(f['wifi'][ap]['rssi'])
                if rssi < 0 and rssi > -91:
                    # Linear values
#                       rssi = rssi - min_rssi
#                     # Exponential values
                    positive = rssi - min_rssi
                    rssi = pow(positive, math.e)/pow(-min_rssi, math.e)
                else:
                    rssi = 0
                rss[ap].append(rssi)
        rssi_v.append(rss)
    return rssi_v


""" Plot similarity (only Sorensen used). Params:
    * index - the index in the collection array. All collection are compared with it
    * method - the method used for rssi value. Examples:
        * 'First'
        * 'Average'
"""

def similarity_collection_vs_all(json_file, collections, index = 0, method = 'First'):
    rssi_v = get_rssi_from_collections(json_file, collections)
    sorensen_plot = []

    for r in range(len(rssi_v)):
        if r == index:
            continue
        rss_1 = []
        rss_2 = []
        ap_comune = 0
        only_1 = 0
        only_2 = 0
        for key in rssi_v[index].keys():

            # Both collections should see the AP;
            if not rssi_v[index][key] or not rssi_v[r][key]:
                continue

            ap_comune+=1
            # Take only the first value
            if method == 'First':
                rss_1.append(rssi_v[index][key][0])
                rss_2.append(rssi_v[r][key][0])

            if method == 'Average':
                rss_1.append(np.average(rssi_v[index][key]))
                rss_2.append(np.average(rssi_v[r][key]))

        print("AP comune = ", ap_comune)
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
