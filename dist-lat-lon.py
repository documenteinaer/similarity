
import math
import json

PI = 3.14159265359


# https://en.wikipedia.org/wiki/Haversine_formula
def dist_haversine(lat1, lon1, lat2, lon2): 
    R = 6371.009 # Radius of earth in KM - WGS84
#    R = 6378.245 # Radius of earth in KM - Romania 
    dLat = lat2 * PI / 180 - lat1 * PI / 180
    dLon = lon2 * PI / 180 - lon1 * PI / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * PI / 180) * math.cos(lat2 * PI / 180) *  math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000 # meters


def dist_haversine_3D(lat1, lon1, ele1, lat2, lon2, ele2):
    # only for short distances (no Earth curvature) 
    return math.sqrt(dist_haversine(lat1, lon1, lat2, lon2)**2 + (ele2-ele1)**2)

print("Haversine3D = ", dist_haversine_3D(44.435191, 26.047582, 84, 44.435191, 26.047582,87))

print("Haversine = ", dist_haversine(44.435191, 26.047582, 44.435198, 26.047961))








