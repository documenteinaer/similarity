
from math import sin, cos, sqrt, radians, atan2, degrees, pi
import utils
"""
Comparisons:  
 formulas collected from web vs. pyproj library
 Haversine vs Euclidean + pyproj  
"""

PI = pi # 3.14159265359
R = 6378137 # radius
e = 8.1819190842622e-2  # eccentricity

R2 = pow(R,2)
e2 = pow(e,2)


def lla2ecef(lat,lon,alt):
    N = R / sqrt(1 - e2 * pow(sin(radians(lat)), 2))
    x = (N + alt) * cos(radians(lat)) * cos(radians(lon))
    y = (N + alt) * cos(radians(lat) )* sin(radians(lon))
    z = ((1 - e2) * N + alt) * sin(radians(lat))
    return x,y,z


def ecef2lla(x, y, z):

  b = sqrt( R2 * (1-e2) )
  bsq = pow(b,2)
  ep = sqrt( (R2 - bsq)/bsq)
  p = sqrt( pow(x,2) + pow(y,2) )
  th = atan2(R*z, b*p)

  lon = atan2(y,x)
  lat = atan2( (z + pow(ep,2)*b*pow(sin(th),3) ), (p - e2*R*pow(cos(th),3)) )
  N = R/( sqrt(1-e2*pow(sin(lat),2)) )
  alt = p / cos(lat) - N

  # mod lat to 0-2pi
  lon = lon % (2*PI)

  return degrees(lat), degrees(lon), alt

def distance_euclidean_3D(x1, y1, z1, x2, y2, z2):
    return(sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2))


# https://en.wikipedia.org/wiki/Haversine_formula
def dist_haversine(lat1, lon1, lat2, lon2): 
    R = 6378.137 # Radius of earth in KM - WGS84
#    R = 6378.245 # Radius of earth in KM - Romania 
    dLat = lat2 * PI / 180 - lat1 * PI / 180
    dLon = lon2 * PI / 180 - lon1 * PI / 180
    a = sin(dLat/2) * sin(dLat/2) + cos(lat1 * PI / 180) * cos(lat2 * PI / 180) *  sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c
    return d * 1000 # meters


def dist_haversine_3D(lat1, lon1, ele1, lat2, lon2, ele2):
    # only for short distances (no Earth curvature) 
    return sqrt(dist_haversine(lat1, lon1, lat2, lon2)**2 + (ele2-ele1)**2)

def dist_ecef_2D(lat1, lon1, lat2, lon2):
    x1,y1,_ = utils.laloal_to_ecef(lat1, lon1, 0)
    x2,y2,_ = utils.laloal_to_ecef(lat2, lon2, 0)
    return distance_euclidean_3D(x1, y1, 0, x2, y2, 0)

def dist_ecef_3D(lat1, lon1, alt1, lat2, lon2, alt2):
    x1,y1,z1 = utils.laloal_to_ecef(lat1, lon1, alt1)
    x2,y2,z2 = utils.laloal_to_ecef(lat2, lon2, alt2)
    return distance_euclidean_3D(x1, y1, z1, x2, y2, z2)



print("Haversine3D = ", dist_haversine_3D(44.435191, 26.047582, 84, 44.435191, 26.047582,87))
print("ECEF 3D = ", dist_ecef_3D(44.435191, 26.047582, 84, 44.435191, 26.047582,87))

print("Haversine = ", dist_haversine(44.435191, 26.047582, 44.435198, 26.047961))
print("ECEF 2D = ", dist_ecef_2D(44.435191, 26.047582, 44.435198, 26.047961))

print("ECEF1 = ", utils.laloal_to_ecef(44.435191, 26.047582, 84))
print("ECEF2 = ", lla2ecef(44.435191, 26.047582, 84))

print("lla = ", utils.ecef_to_laloal(4098468.2450743783, 2003171.523662474, 4442807.553680874))
print("lla2 = ", ecef2lla(4098468.2450743783, 2003171.523662474, 4442807.553680874))




