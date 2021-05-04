#!/bin/python
"""
    Preprocessing phase consists of:
        * Takes a json file and creates another one with "r_" preceded;
        * For every collection/location transform the array of fingerprints
            into a single fingerprint;
        * Reads _whitelist.json_ file and replaces the equivalences;
"""

import sys
import json
import math



def transform_rssi(rssi):
    return rssi
#     min_rssi = -100
#     positive = rssi - min_rssi
#     return pow(positive, math.e)/pow(-min_rssi, math.e)

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print(sys.argv[0], " whitelist.json inputfile.json [orientation N/S/E/V]")
    print("Produces p_inputfile.json")
    sys.exit(1)
    
json_file = sys.argv[2]
wl_file = sys.argv[1]
    
f = open(json_file)
data = json.load(f)
w = open(wl_file, 'r')
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
        if len(sys.argv) == 4:
            if i > int(sys.argv[3]):
                continue
        eq_mac = None
        for mac in f["wifi"].keys():
            for key in w_list:
                    if mac in w_list[key]:
                        eq_mac = key

            if not eq_mac:
                continue
            # If new MAC, add it to the collection
            if not eq_mac in fingerprint["wifi"]:
                fingerprint["wifi"][eq_mac] = f["wifi"][mac]
                fingerprint["wifi"][eq_mac]['rssi'] = [transform_rssi(int(f["wifi"][mac]['rssi']))]
            else: # If existing MAC, add only the rssi value

                # If rssi is a string, transform it to an 1 element array
                if isinstance(fingerprint["wifi"][eq_mac]["rssi"], str):
                    fingerprint["wifi"][eq_mac]["rssi"] = [transform_rssi(int(f["wifi"][mac]["rssi"]))]

                # If rssi is an array, add the rssi value to array
                if isinstance(fingerprint["wifi"][eq_mac]["rssi"], list):
                    fingerprint["wifi"][eq_mac]["rssi"].append(transform_rssi(int(f["wifi"][mac]["rssi"])))

        for mac in f["ble"].keys():
            if not mac in fingerprint["ble"]:
                fingerprint["ble"][mac] = f["ble"][mac]


    collection["fingerprints"] = fingerprint
    collections[c] = collection

if len(sys.argv) == 4:
    with open("p"+sys.argv[3]+"_"+json_file, "w+") as outfile:
        json.dump(collections, outfile, indent = 4)
else:
    with open("p_"+json_file, "w+") as outfile:
        json.dump(collections, outfile, indent = 4)

outfile.close()

