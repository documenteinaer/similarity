#!/usr/bin/env python3 

import pyproj
import math 

coords = [ # lat lon alt 
  (37.4001100556,  -79.1539111111,  208.38),
  (37.3996955278,  -79.153841,  208.48),
  (37.3992233889,  -79.15425175,  208.18),
  (37.3989114167,  -79.1532775833,  208.48),
  (37.3993285556,  -79.1533773333,  208.28),
  (37.3992801667,  -79.1537883611,  208.38),
  (37.3992441111,  -79.1540981944,  208.48),
  (37.3992616389,  -79.1539428889,  208.58),
  (37.3993530278,  -79.1531711944,  208.28),
  (37.4001223889,  -79.1538085556,  208.38),
  (37.3992922222,  -79.15368575,  208.28),
  (37.3998074167,  -79.1529132222,  208.18),
  (37.400068,  -79.1542711389,  208.48),
  (37.3997516389,  -79.1533794444,  208.38),
  (37.3988933333,  -79.1534320556,  208.38),
  (37.3996279444,  -79.154401,  208.58),
]

transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:4978") 

def ecef_to_laloal(x, y, z): # returns latitude longitude altitude (meters) 
    return transformer.transform(x, y, z, direction='INVERSE')


def laloal_to_ecef_pyproj(lat, lon, alt): # returns x y z (meters)
    return transformer.transform(lat, lon, alt)


def laloal_to_ecef_custom(lat, lon, alt):
    rad_lat = lat * (math.pi / 180.0)
    rad_lon = lon * (math.pi / 180.0)

    a = 6378137.0
    finv = 298.257223563
    f = 1 / finv
    e2 = 1 - (1 - f) * (1 - f)
    v = a / math.sqrt(1 - e2 * math.sin(rad_lat) * math.sin(rad_lat))

    x = (v + alt) * math.cos(rad_lat) * math.cos(rad_lon)
    y = (v + alt) * math.cos(rad_lat) * math.sin(rad_lon)
    z = (v * (1 - e2) + alt) * math.sin(rad_lat)
    return x, y, z


def run_test():

    for pt in coords:
        ecef1 = laloal_to_ecef_pyproj(pt[0], pt[1], pt[2])
        ecef2 = laloal_to_ecef_custom(pt[0], pt[1], pt[2])
        print('pyproj', ecef1)
        print('custom', ecef2)
        print('pt', pt)
        print('rev', ecef_to_laloal(ecef1[0], ecef1[1], ecef1[2])) 

run_test()

