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
import scipy.stats as st
import random
import cv2
import difflib


min_rssi = -100

"""
Takes the original json file and creates a new json file with the fingerprints array merged
into a single json element.
"""


def preprocessing(json_file):

    f = open(json_file)
    data = json.load(f)
    w = open('whitelist.json', 'r')
    w_list = json.load(w)
    collections = {}

#     while 'collection'+str(coll_no) in data:
    for c in data.keys():
        collection = data[c]

        # Transform array of fingerprints into a single fingerprint
        fingerprints = collection['fingerprints']
        if not fingerprints:
            continue
#         fingerprint = fingerprints[0]

        fingerprint = {}
        if 'timestamp' in fingerprints[0]:
            fingerprint['timestamp'] = fingerprints[0]['timestamp']
        fingerprint['wifi'] = {}
        if 'ble' in fingerprints[0]:
            fingerprint['ble'] = fingerprints[0]['ble']
        if 'gps' in fingerprints[0]:
            fingerprint['gps'] = fingerprints[0]['gps']
        if 'telephony' in fingerprints[0]:
            fingerprint['telephony'] = fingerprints[0]['telephony']


        for i,f in enumerate(fingerprints):
            if i==0:
                continue
            eq_mac = None
            for mac in f["wifi"].keys():
                for key in w_list:
                    if mac in w_list[key]:
                        eq_mac = key

                if not eq_mac:
                    print("Lipsește", mac)
                    continue
                # If new MAC, add it to the collection
                if not eq_mac in fingerprint["wifi"]:
                    fingerprint["wifi"][eq_mac] = f["wifi"][mac]
                    fingerprint["wifi"][eq_mac]['rssi'] = [int(f["wifi"][mac]['rssi'])]
                else: # If existing MAC, add only the rssi value

                    # If rssi is a string, transform it to an 1 element array
                    if isinstance(fingerprint["wifi"][eq_mac]["rssi"], str):
                        fingerprint["wifi"][eq_mac]["rssi"] = [int(f["wifi"][mac]["rssi"])]

                    # If rssi is an array, add the rssi value to array
                    if isinstance(fingerprint["wifi"][eq_mac]["rssi"], list):
                        fingerprint["wifi"][eq_mac]["rssi"].append(int(f["wifi"][mac]["rssi"]))

            for mac in f["ble"].keys():
                if not mac in fingerprint["ble"]:
                    fingerprint["ble"][mac] = f["ble"][mac]


        collection["fingerprints"] = fingerprint
        collections[c] = collection

    with open("p_"+json_file, "w+") as outfile:
        json.dump(collections, outfile, indent = 4)
    outfile.close()


def get_all_APs_in_json(json_file, whitelist = False):
    APs = []
    f = open("p_"+json_file, 'r')
    data = json.load(f)
    w = open('whitelist.json', 'r')
    whitelist_ap = json.load(w)

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

    f = open(json_file, 'r')
    data = json.load(f)

    for col in data.keys():
        fingerprint = data[col]['fingerprints']

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
            for f in c['fingerprints']['wifi']:
                if not ap in f:
                    continue
                if type(c['fingerprints']['wifi'][f]['rssi']) is list:
                    for rssi in c['fingerprints']['wifi'][f]['rssi']:
                        if rssi < 0 and rssi > -91:
                            # Linear values
#                               rssi = rssi - min_rssi
                              # Exponential values
                              positive = rssi - min_rssi
                              rssi = pow(positive, math.e)/pow(-min_rssi, math.e)
                        else:
                            rssi = 0
                        rss[ap].append(rssi)
                else:
                    rssi = c['fingerprints']['wifi'][f]['rssi']
                    if int(rssi) < 0 and int(rssi) > -91:
                        # Linear values
#                           rssi = int(rssi) - min_rssi
                          # Exponential values
                          positive = int(rssi) - min_rssi
                          rssi = pow(positive, math.e)/pow(-min_rssi, math.e)
                    else:
                        rssi = 0

                    rss[ap].append(rssi)
        rssi_v.append(rss)
    return rssi_v


def np_hist_to_cv(np_histogram_output):
    counts, bin_edges = np_histogram_output
    return counts.ravel().astype('float32')


def chi2_distance(histA, histB, eps = 1e-10):
    # compute the chi-squared distance
    d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
        for (a, b) in zip(histA, histB)])
    # return the chi-squared distance
    return d



""" Plot similarity (only Sorensen used). Params:
    * index - the index in the collection array. All collection are compared with it
    * method - the method used for rssi value. Examples:
        * 'First'
        * 'Average'
"""

def similarity_collection_vs_all(json_file, collections, index, method = 'First', label = None):
    rssi_v = get_rssi_from_collections(json_file, collections)
    sorensen_plot = []
    result = []

    for r in range(len(rssi_v)):
        if r == index:
            # The similarity = 0
            sorensen_plot.append(0)
            continue
        rss_1 = []
        rss_2 = []
        ap_comune = 0
        only_1 = 0
        only_2 = 0
        chi = 0


        for key in rssi_v[index].keys():

            # Both collections should see the AP;
            if not rssi_v[index][key] or not rssi_v[r][key]:
                continue

            ap_comune += 1


            # Take only the first value
            if method == 'First':
                rss_1.append(rssi_v[index][key][0])
                rss_2.append(rssi_v[r][key][0])

            if method == 'Average':
                rss_1.append(np.average(rssi_v[index][key]))
                rss_2.append(np.average(rssi_v[r][key]))

            # Select random RSSI values from each AP
            if method[:6] == 'Random':
                no_of_random_elements = int(method[6:])

                if len(rssi_v[index][key]) >= no_of_random_elements:
                    rss_1.append(np.average(random.choices(rssi_v[index][key], k=no_of_random_elements)))
                else:
                    rss_1.append(np.average(rssi_v[index][key]))
                if len(rssi_v[index][key]) >= no_of_random_elements:
                    rss_2.append(np.average(random.choices(rssi_v[r][key], k=no_of_random_elements)))
                else:
                    rss_2.append(np.average(rssi_v[r][key]))

            if method == 'Median':
                rss_1.append(np.median(rssi_v[index][key]))
                rss_2.append(np.mean(rssi_v[r][key]))

            if method == 'Chi-squared':
                chi += chi2_distance(rssi_v[index][key], rssi_v[r][key])

            if method == 'Tempered':
                rss_1.append(np.average(rssi_v[index][key]) * random.uniform(0.8, 1.2))
                rss_2.append(np.average(rssi_v[r][key]) * random.uniform(0.8, 1.2))


        if method != 'Chi-squared' and not rss_1 or ap_comune * 10 < len(rssi_v[index].keys()):
            # If not enough common AP, similarity = 1
            sorensen_plot.append(1)
            continue
        if method == 'Chi-squared':
            sorensen_plot.append(chi)
        else:
            if braycurtis(tuple(rss_1), tuple(rss_2)) < 0.1:
                result.append(r)
            sorensen_plot.append(braycurtis(tuple(rss_1), tuple(rss_2)))

#     print(sorensen_plot)
    if label:
        plt.plot(sorensen_plot, 'o', label = label)
    else:
        plt.plot(sorensen_plot, 'o', label = method)

    plt.xlabel("Nr. crt.")
    plt.ylabel("Similarity Measurement")
    plt.legend()
    plt.show()

    return result

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
