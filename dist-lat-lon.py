
import math
import json

PI = 3.14159265359

def dist_lat_lon(Lat1, Lon1, Lat2, Lon2):

# http://en.wikipedia.org/wiki/Lat-lon
# Approximate computation for short distances 
# Wikipedia entry states that the distance  estimates are within 0.6m for 100km longitudinally and 1cm for 100km latitudinally

    latMid = (Lat1+Lat2)/2.0;  # or just use Lat1 for slightly less accurate estimate

    m_per_deg_lat = 111132.954 - 559.822 * math.cos( 2.0 * latMid ) + 1.175 * math.cos( 4.0 * latMid)
    m_per_deg_lon = (PI/180 ) * 6367449 * math.cos ( latMid )

    deltaLat = abs(Lat1 - Lat2)
    deltaLon = abs(Lon1 - Lon2)

    return math.sqrt ((deltaLat * m_per_deg_lat)**2 + (deltaLon * m_per_deg_lon)**2)


# https://en.wikipedia.org/wiki/Haversine_formula
def dist_haversine(lat1, lon1, lat2, lon2): 
    R = 6378.137 # Radius of earth in KM
    dLat = lat2 * PI / 180 - lat1 * PI / 180
    dLon = lon2 * PI / 180 - lon1 * PI / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * PI / 180) * math.cos(lat2 * PI / 180) *  math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000 # meters



#fObj = open('27-01-2021_19-19-59.json',)
#$p = json.load(fObj)

print("Simplified = ", dist_lat_lon(44.45204367, 26.10662322, 44.45204923, 26.10661848))

print("Haverside = ", dist_haversine(44.45204367, 26.10662322, 44.45204923, 26.10661848))

#for i in p['data']:
#    print(i)







