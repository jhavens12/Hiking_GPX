import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBcs730quQqEapBEjicXLLxaChTseXs_fA"
import pdb
import datetime
import sys as mod_sys
import logging as mod_logging
import math as mod_math
import glob
import gpxpy as mod_gpxpy
from pprint import pprint
import gpxpy.geo
import calculations
import geocoder

#modified to work with single track GPX files - missing calculations
#Adds elevation data to gpx sections that are misssing it
#does not work with fitness information (time,pace,HR)

def meters_to_feet(meters):
    meters_int = int(meters)
    feet1 = meters_int / 0.3048
    feet2 = ("{0:.2f}".format(feet1))
    return feet2
#need to add autoconvert to miles?

def meters_to_miles(meters):
    meters_int = int(meters)
    miles1 = meters_int * 0.000621371
    miles2 = ("{0:.2f}".format(miles1))
    return miles2

def convert_HMS(i):
    m, s = divmod(i, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def feet_to_miles(i):
    return i*0.000189393939

def seconds_to_minutes(i):
    return float(i/60)


def print_gpx_info(gpx, gpx_file):
    dict1 = {}
    #print('File: %s' % gpx_file)
    dict1['file'] = gpx_file
    if gpx.name:
        dict1['gpx_name'] = gpx.name
    if gpx.description:
        dict1['gpx_description'] = gpx.description
    if gpx.author_name:
        dict1['gpx_author_name'] = gpx.author_name
    if gpx.author_email:
        dict1['gpx_author_email'] = gpx.author_email
    waypoints = {}
    if gpx.waypoints:
        for waypoint in gpx.waypoints:
            #print ('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))
            waypoints['name'] = waypoint.name
            waypoints['latitude'] = waypoint.latitude
            waypoints['longitude'] = waypoint.longitude
            waypoints['symbol'] = waypoint.symbol
            waypoints['elevation'] = waypoint.elevation
            waypoints['description'] = waypoint.description
    dict1['waypoints'] = waypoints

    #performanace based measurement
    dict1['moving_time'], dict1['stopped_time'], dict1['moving_distance_meters'], dict1['stopped_distance_meters'], dict1['max_speed'] = gpx.get_moving_data()
    dict1['start_time'], dict1['end_time'] = gpx.get_time_bounds()
    if dict1['moving_time']:
        dict1['moving_time_HMS'] = convert_HMS(dict1['moving_time'])
    else:
        print (dict1['file'],"does not contain moving_time")
    if dict1['moving_distance_meters']:
        dict1['moving_distance_miles'] = meters_to_miles(dict1['moving_distance_meters'])
    else:
        print (dict1['file'],"does not contain moving_distance_meters")
    if dict1['stopped_time']:
        dict1['stopped_time_HMS'] = convert_HMS(dict1['stopped_time'])
    else:
        print (dict1['file'],"does not contain stopped_time")
    if dict1['stopped_distance_meters']:
        dict1['stopped_distance_miles'] = meters_to_miles(dict1['stopped_distance_meters'])
    else:
        print (dict1['file'],"does not contain stopped_distance_meters")

    dict1['length_2d'] = gpx.length_2d()
    dict1['length_3d'] = gpx.length_3d()

    dict1['uphill'], dict1['downhill'] = gpx.get_uphill_downhill()
    dict1['points_no'] = len(list(gpx.walk(only_points=True)))

    dict1['length_2d_miles'] = meters_to_miles(dict1['length_2d'])
    dict1['length_3d_miles'] = meters_to_miles(dict1['length_3d'])

    dict1['uphill_feet'] = meters_to_feet(dict1['uphill'])
    dict1['downhill_feet'] = meters_to_feet(dict1['downhill'])


    if dict1['points_no'] > 0:
        distances = []
        previous_point = None
        for point in gpx.walk(only_points=True):
            if previous_point:
                distance = point.distance_2d(previous_point)
                distances.append(distance)
            previous_point = point
        dict1['points_distance'] = sum(distances) / len(list(gpx.walk()))
        dict1['segments'] = {}
    for track_no, track in enumerate(gpx.tracks):
        for segment_no, segment in enumerate(track.segments):
            var3 = "track_"+str(track_no)+"_"+"seg_"+str(segment_no)
            dict1['segments'][var3] = gpx_track_seg_info(segment,track_no,segment_no,track)
            #dict1['segments'][var3]['name'] = track.name
    return dict1




def gpx_track_seg_info(gpx_part,track_no,segment_no,track):
    #run for each segment in gpx file
    seg_dict = {}
    seg_dict['name'] = track.name
    seg_dict['moving_time'], seg_dict['stopped_time'], seg_dict['moving_distance_meters'], seg_dict['stopped_distance_meters'], seg_dict['max_speed'] = gpx_part.get_moving_data()
    seg_dict['length_2d'] = gpx_part.length_2d()
    seg_dict['length_3d'] = gpx_part.length_3d()
    seg_dict['uphill'], seg_dict['downhill'] = gpx_part.get_uphill_downhill()
    seg_dict['points_no'] = len(list(gpx_part.walk(only_points=True)))
    seg_dict['start_time'], seg_dict['end_time'] = gpx_part.get_time_bounds()


    seg_dict['length_2d_miles'] = meters_to_miles(seg_dict['length_2d'])
    seg_dict['length_3d_miles'] = meters_to_miles(seg_dict['length_3d'])

    seg_dict['uphill_feet'] = meters_to_feet(seg_dict['uphill'])
    seg_dict['downhill_feet'] = meters_to_feet(seg_dict['downhill'])

    if seg_dict['moving_time']:
        seg_dict['moving_time_HMS'] = convert_HMS(seg_dict['moving_time'])
    else:
        #print (seg_dict['name'],"does not contain moving_time")
        seg_dict['moving_time_HMS'] = 0
    if seg_dict['moving_distance_meters']:
        seg_dict['moving_distance_miles'] = meters_to_miles(seg_dict['moving_distance_meters'])
    else:
        #print (seg_dict['name'],"does not contain moving_distance_meters")
        seg_dict['moving_distance_miles'] = 0
    if seg_dict['stopped_time']:
        seg_dict['stopped_time_HMS'] = convert_HMS(seg_dict['stopped_time'])
    else:
        #print (seg_dict['name'],"does not contain stopped_time")
        seg_dict['stopped_time_HMS'] = 0
    if seg_dict['stopped_distance_meters']:
        seg_dict['stopped_distance_miles'] = meters_to_miles(seg_dict['stopped_distance_meters'])
    else:
        #print (seg_dict['name'],"does not contain stopped_distance_meters")
        seg_dict['stopped_distance_miles'] = 0

    if seg_dict['points_no'] > 0:
        distances = []
        previous_point = None
        for point in gpx_part.walk(only_points=True):
            if previous_point:
                distance = point.distance_2d(previous_point)
                distances.append(distance)
            previous_point = point
        seg_dict['points_distance'] = sum(distances) / len(list(gpx_part.walk()))
    #point dictionary creation for each segment
    point_dict = {}
    for s,point in enumerate(gpx_part.points):
        n=s+1
        point_dict[n] = {}
        point_dict[n]['latitude'] = point.latitude
        point_dict[n]['longitude'] = point.longitude
        point_dict[n]['elevation'] = point.elevation
        point_dict[n]['time'] = point.time

    first_point = 1
    #below adds elevation delta to dictionary from start of segment


    if point_dict[1]['elevation'] == None:
        print(track.name,"Has no elevation data")
        # for point in list(sorted(point_dict)):
        #     #print(point_dict[point]['longitude'],point_dict[point]['latitude'])
        #     g = geocoder.google([point_dict[point]['latitude'], point_dict[point]['longitude']], method='elevation')
        #     #print(g.meters)
        #     point_dict[point]['elevation'] = g.meters

    if point_dict[1]['elevation'] != None:
    #if point.elevation != None:
        for point in point_dict:
            point_dict[point]['elevation_delta'] = point_dict[point]['elevation'] - point_dict[first_point]['elevation']
            point_dict[point]['elevation_feet'] = float(meters_to_feet(point_dict[point]['elevation']))
            point_dict[point]['elevation_delta_feet'] = point_dict[point]['elevation_feet'] - point_dict[first_point]['elevation_feet']

    for point in list(sorted(point_dict)):
        if point >=2:
            previous_point = point - 1
            point_dict[point]['distance_from_previous'] = calculations.distance(point_dict[point]['latitude'], \
            point_dict[point]['longitude'], point_dict[point]['elevation'], \
            point_dict[previous_point]['latitude'], point_dict[previous_point]['longitude'], \
            point_dict[previous_point]['elevation'], haversine=None)
            point_dict[point]['distance_from_start'] = point_dict[previous_point]['distance_from_start'] + point_dict[point]['distance_from_previous']
            point_dict[point]['distance_from_start_feet'] = float(meters_to_feet(point_dict[point]['distance_from_start']))
            point_dict[point]['distance_from_start_miles'] = float(feet_to_miles(point_dict[point]['distance_from_start_feet']))
        else:
            point_dict[point]['distance_from_start_feet'] = 0
            point_dict[point]['distance_from_previous'] = 0
            point_dict[point]['distance_from_start'] = 0
            point_dict[point]['distance_from_start_miles'] = 0
        if point_dict[point]['time']:
            if seg_dict['start_time']:
                point_dict[point]['time_delta'] = point_dict[point]['time'] - seg_dict['start_time']
                point_dict[point]['time_delta_seconds'] = point_dict[point]['time_delta'].seconds
                point_dict[point]['time_delta_minutes'] = seconds_to_minutes(point_dict[point]['time_delta_seconds'])
            else:
                #print(seg_dict['name']+" does not contain start_time")
                point_dict[point]['time_delta'] = 0
                point_dict[point]['time_delta_seconds'] = 0
                point_dict[point]['time_delta_minutes'] = 0
        else:
            #print(str(point)+" in "+seg_dict['name']+" does not contain time")
            point_dict[point]['time_delta'] = 0
            point_dict[point]['time_delta_seconds'] = 0
            point_dict[point]['time_delta_minutes'] = 0

    #pprint(point_dict)
    seg_dict['data_points'] = point_dict

    return seg_dict

def run(gpx_files):
    master_dict = {}
    if not gpx_files:
        print('No GPX files given')
        mod_sys.exit(1)

    for gpx_file in gpx_files:
        try:
            gpx = mod_gpxpy.parse(open(gpx_file))
            dict1 = print_gpx_info(gpx, gpx_file)
            key1 = dict1['file'] #sets key to be the start time for each GPX file
            master_dict[key1] = dict1

        except Exception as e:
            mod_logging.exception(e)
            print('Error processing %s' % gpx_file)
            mod_sys.exit(1)
    return master_dict


if __name__ == '__main__':
    #run(mod_sys.argv[1:])
    run(file_list) #accepts file list from outside program
    #run()
