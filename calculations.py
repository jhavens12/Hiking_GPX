import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBcs730quQqEapBEjicXLLxaChTseXs_fA"

import math as mod_math

ONE_DEGREE = 1000. * 10000.8 / 90.
EARTH_RADIUS = 6371 * 1000

def distance(latitude_1, longitude_1, elevation_1, latitude_2, longitude_2, elevation_2, haversine=None):
    # If points too distant -- compute haversine distance:
    if haversine or (abs(latitude_1 - latitude_2) > .2 or abs(longitude_1 - longitude_2) > .2):
        return haversine_distance(latitude_1, longitude_1, latitude_2, longitude_2)

    coef = mod_math.cos(latitude_1 / 180. * mod_math.pi)
    x = latitude_1 - latitude_2
    y = (longitude_1 - longitude_2) * coef

    distance_2d = mod_math.sqrt(x * x + y * y) * ONE_DEGREE

    if elevation_1 is None or elevation_2 is None or elevation_1 == elevation_2:
        return distance_2d

    return mod_math.sqrt(distance_2d ** 2 + (elevation_1 - elevation_2) ** 2)

def get_elevation(point_dict):
    if point_dict[1]['elevation'] == None:
        for point in list(sorted(point_dict)):
            print(point_dict[point]['longitude'],point_dict[point]['latitude'])
            g = geocoder.google([point_dict[point]['latitude'], point_dict[point]['longitude']], method='elevation')
            print(g.meters)
            point_dict[point]['elevation'] = g.meters
    else:
        print ("elevation data exists, bruh")
