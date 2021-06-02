#!/usr/bin/env python3

"""
    Preprocessing phase consists of:
        * Takes a json file and creates another one with "r_" preceded;
        * For every collection/location transform the array of fingerprints
            into a single fingerprint;
        * Reads _whitelist.json_ file and replaces the equivalences;
"""

import sys, argparse, datetime
import json
import math
import utils 
import os

inputfile = ''
outputfile = ''
whitelistfile = ''

def parse_opt():
    parser = argparse.ArgumentParser()

    # By default it will fail with multiple arguments.
    parser.add_argument('-i', action='store', dest='inputfile' )
    parser.add_argument('-o', action='store', dest='outputfile' )
    parser.add_argument('-wwl', action='store', dest='w_whitelistfile', help='WiFi whitelist' )
    parser.add_argument('-bwl', action='store', dest='b_whitelistfile', help='BLE whitelist' )
    parser.add_argument('-gwl', action='store_true', help='generates a plain whitelist, \
each mac has itself in the list; uses -o argument for output' )
    parser.add_argument('-diff', action='store', dest='inputfile2', help='INPUTFILE-INPUTFILE2, \
wifi MACs only in INPUTFILE')
    parser.add_argument('-cf', nargs='+', type=int, help='combine fingerprints:\
[-1] means no combining; \
0 means first fingerprint in each collection;\
rssi values are sorted;\
') 
    parser.add_argument('-gps2ecef', action='store_true', help='lat,long,ele -> x,y,z')
    parser.add_argument('-ecef2gps', action='store_true', help='x,y,z, -> lat,long,ele')
    parser.add_argument('-interp', action='store_true', help='generates locations(gps&ecef) \
for fingerprints that dont have using the ones that do. Assumes straight lines and equidistance')
    parser.add_argument('--floor', action='store_true',  help='Break input file by floors')


    args = parser.parse_args()

    #for x, value in args._get_kwargs():
    #    print(x,"=", value)
    return args


args = parse_opt()


def transform_rssi(rssi):
    return rssi
#     min_rssi = -100
#     positive = rssi - min_rssi
#     return pow(positive, math.e)/pow(-min_rssi, math.e)


def combine_fp(data, combine):
    """
    combine = [-1] accept all 
    combine = [0 2 (n-1) ] merges these fps (all collections should have n fps)
    """
    collections = {}
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


        for nf,f in enumerate(fingerprints):
            if combine[0] != -1: 
                if nf not in combine:
                    continue

            for mac in f["wifi"].keys():

                lf = []
                if isinstance(f["wifi"][mac]["rssi"], str):
                    lf = [int(f["wifi"][mac]['rssi'])]
                if isinstance(f["wifi"][mac]["rssi"], int):
                    lf = [f["wifi"][mac]['rssi']]
                if isinstance(f["wifi"][mac]["rssi"], list):
                    lf.extend(f["wifi"][mac]['rssi'])

                if not mac in fingerprint["wifi"]:
                    fingerprint["wifi"][mac] = f["wifi"][mac]
                    fingerprint["wifi"][mac]['rssi'] = []

                fingerprint["wifi"][mac]['rssi'].extend(lf)
                fingerprint["wifi"][mac]['rssi'].sort()

            for mac in f["ble"].keys():
                if not mac in fingerprint["ble"]:
                    fingerprint["ble"][mac] = f["ble"][mac]


        collection["fingerprints"] = [fingerprint]
        collections[c] = collection 
    return collections 

###########################################################

def apply_wl(data, w_list):
    collections = {}
    for c in data.keys():
        collection = data[c]

        # Transform array of fingerprints into a single fingerprint
        fingerprints = collection['fingerprints']
        if not fingerprints:
            continue

        collection["fingerprints"] = []
        for nf,f in enumerate(fingerprints):
            fingerprint = {}
            if 'timestamp' in f:
                fingerprint['timestamp'] = f['timestamp']
            fingerprint['wifi'] = {}
            if 'ble' in f:
                fingerprint['ble'] = f['ble']
            if 'gps' in f:
                fingerprint['gps'] = f['gps']
            if 'telephony' in f:
                fingerprint['telephony'] = f['telephony']

            eq_mac = None
            for mac in f["wifi"].keys():
                if len(w_list) == 0: # no white list, therefore accept all 
                    eq_mac = mac
                else:    
                    for key in w_list:
                        if mac in w_list[key]:
                            eq_mac = key

                if not eq_mac:
                    continue
                # If new MAC, add it to the collection

                lf = []
                if isinstance(f["wifi"][mac]["rssi"], str):
                    lf = [int(f["wifi"][mac]['rssi'])]
                if isinstance(f["wifi"][mac]["rssi"], int):
                    lf = [f["wifi"][mac]['rssi']]
                if isinstance(f["wifi"][mac]["rssi"], list):
                    lf.extend(f["wifi"][mac]['rssi'])

                if not eq_mac in fingerprint["wifi"]:
                    fingerprint["wifi"][eq_mac] = f["wifi"][mac]
                    fingerprint["wifi"][eq_mac]['rssi'] = []

                fingerprint["wifi"][eq_mac]['rssi'].extend(lf)
                fingerprint["wifi"][eq_mac]['rssi'].sort()

            for mac in f["ble"].keys():
                if not mac in fingerprint["ble"]:
                    fingerprint["ble"][mac] = f["ble"][mac]

            collection["fingerprints"].append(fingerprint)

        collections[c] = collection
    return collections 



def generate_whitelist(data):
    collections = {}
    for c in data.keys():
        collection = data[c]

        for nf,f in enumerate(data[c]["fingerprints"]):
            for mac in f["wifi"].keys():
                if not mac in collections.keys():
                    collections[mac]=[mac, f["wifi"][mac]["ssid"], f["wifi"][mac]["frequency"]]
    return collections

def col_diff(data, data2):
    collections = {}
    for c in data.keys():
        if c in data2.keys(): 
            for nf,f in enumerate(data[c]["fingerprints"]):
                for mac in f["wifi"].keys():
                    found = False
                    for nf2,f2 in enumerate(data2[c]["fingerprints"]):
                        if mac in f2["wifi"].keys():
                            found = True
                            break
                        if not found:
                            collections[mac]=[f["wifi"][mac]["ssid"], f["wifi"][mac]["frequency"], c]


    return collections 


def interp(data):
    out = {}
    prevx = 0.0 
    prevy = 0.0 
    prevz = 0.0 
    cols = []
    for c in data.keys():
        if "x" in data[c]:
            if (math.fabs(data[c]["x"]) < 0.001) and (math.fabs(data[c]["y"]) < 0.001):
                cols.append(data[c])
            else:
                n = 1
                for sc in cols:
                    sc["x"] = prevx + (float(data[c]["x"]) - prevx)*n/(1.0+len(cols))
                    sc["y"] = prevy + (float(data[c]["y"]) - prevy)*n/(1.0+len(cols))
                    sc["z"] = prevz # only works on the same floor
                    assert math.fabs(prevz - float(data[c]["z"])) < 0.001
                    n = n + 1
                cols = []
                prevx = data[c]["x"]
                prevy = data[c]["y"]
                prevz = data[c]["z"]
        out[c] = data[c]
    return out

def split_by_floors(data):
    floors = []
    output_file_basename = os.path.basename(args.outputfile)

    for c in data.keys():
        if "z" in data[c] and data[c]["z"] not in floors:
            floors.append(data[c]["z"])

    collections = [None] * len(floors)
    for z in floors:
        collection = {}
        i = 0
        for c in data.keys():
            if "z" in data[c] and z == data[c]["z"]:
                collection["collection"+str(i)] = data[c]
                i += 1

        collections[floors.index(z)] = collection

    for z in floors:
        with open(str(z)+args.outputfile, "w+") as outfile:
            if "proc" not in collections: # add a processing log 
                collections[floors.index(z)]["proc"] = {}
            collections[floors.index(z)]["proc"][str(datetime.datetime.now())] = ' '.join(sys.argv)

            json.dump(collections[floors.index(z)], outfile, indent = 4)
            outfile.close()



# M A I N 
"""    
One action at a time: gwl, whitelist+merge, combine fingerprints
"""
data = json.load(open(args.inputfile))

if args.gwl:
    collections = generate_whitelist(data)
elif args.w_whitelistfile != None:
    w_list = json.load(open(args.w_whitelistfile, 'r'))
    collections = apply_wl(data, w_list)        
elif args.cf != None:
    collections = combine_fp(data, args.cf)
elif args.floor != None:
    split_by_floors(data)
elif args.inputfile2 != None:
    data2 = json.load(open(args.inputfile2))
    collections = col_diff(data, data2)
elif args.interp:
    collections = interp(data) 
else:
    collections = data # unchanged 

if args.floor == None:
    with open(args.outputfile, "w+") as outfile:
        if "proc" not in collections: # add a processing log 
            collections["proc"] = {}
        collections["proc"][str(datetime.datetime.now())] = ' '.join(sys.argv)

        json.dump(collections, outfile, indent = 4)
        outfile.close()

