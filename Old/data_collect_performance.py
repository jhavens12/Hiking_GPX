import pdb

import datetime
import sys as mod_sys
import logging as mod_logging
import math as mod_math
import glob
import gpxpy as mod_gpxpy
from pprint import pprint

#gpx_file = open("Hunger Mountain 2017.10.14.GPX", 'r')
#gpx = gpxpy.parse(gpx_file)



#file_list = glob.glob("/Users/Havens/Dropbox/PYTHON/Hiking2/*.GPX")
#print(file_list)

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

    dict1['length_2d'] = gpx.length_2d()
    dict1['length_3d'] = gpx.length_3d()

    dict1['moving_time'], dict1['stopped_time'], dict1['moving_distance_meters'], dict1['stopped_distance_meters'], dict1['max_speed'] = gpx.get_moving_data()
    dict1['uphill'], dict1['downhill'] = gpx.get_uphill_downhill()
    dict1['start_time'], dict1['end_time'] = gpx.get_time_bounds()
    dict1['points_no'] = len(list(gpx.walk(only_points=True)))

    dict1['total_time'] = dict1['end_time'] - dict1['start_time']

    dict1['length_2d_miles'] = meters_to_miles(dict1['length_2d'])
    dict1['length_3d_miles'] = meters_to_miles(dict1['length_3d'])

    dict1['uphill_feet'] = meters_to_feet(dict1['uphill'])
    dict1['downhill_feet'] = meters_to_feet(dict1['downhill'])

    dict1['moving_time_HMS'] = convert_HMS(dict1['moving_time'])
    dict1['moving_distance_miles'] = meters_to_miles(dict1['moving_distance_meters'])

    dict1['stopped_time_HMS'] = convert_HMS(dict1['stopped_time'])
    dict1['stopped_distance_miles'] = meters_to_miles(dict1['stopped_distance_meters'])

    if dict1['points_no'] > 0:
        distances = []
        previous_point = None
        for point in gpx.walk(only_points=True):
            if previous_point:
                distance = point.distance_2d(previous_point)
                distances.append(distance)
            previous_point = point
        dict1['points_distance'] = sum(distances) / len(list(gpx.walk()))
    #print('')

    #point_dict = {}

    if len(gpx.tracks) > 2:
        for track_no, track in enumerate(gpx.tracks):
            for segment_no, segment in enumerate(track.segments):
                var3 = "track_"+str(track_no)+"_"+"seg_"+str(segment_no)
                dict1[var3] = gpx_track_seg_info(segment,track_no,segment_no)
                dict1[var3]['name'] = track.name
        return dict1
    else:
        for track_no, track in enumerate(gpx.tracks):
            for segment_no, segment in enumerate(track.segments): #for each segment in each track
                var3 = "track_"+str(track_no)+"_"+"seg_"+str(segment_no) #set up var3 to be key of dictionary
                seg_dict = gpx_track_seg_info(segment,track_no,segment_no) #sets key to be the result of gpx_track_seg_info
                seg_dict['name'] = track.name #sets name after function to be track.name
                if seg_dict['ascent']:
                    dict1["ascent"] = seg_dict
                if seg_dict['descent']:
                    dict1["descent"] = seg_dict
        return dict1


def gpx_track_seg_info(gpx_part,track_no,segment_no):
    #run for each segment in gpx file
    dict1 = {}
    dict1['length_2d'] = gpx_part.length_2d()
    dict1['length_3d'] = gpx_part.length_3d()
    dict1['moving_time'], dict1['stopped_time'], dict1['moving_distance_meters'], dict1['stopped_distance_meters'], dict1['max_speed'] = gpx_part.get_moving_data()
    dict1['uphill'], dict1['downhill'] = gpx_part.get_uphill_downhill()
    dict1['start_time'], dict1['end_time'] = gpx_part.get_time_bounds()
    dict1['points_no'] = len(list(gpx_part.walk(only_points=True)))

    dict1['length_2d_miles'] = meters_to_miles(dict1['length_2d'])
    dict1['length_3d_miles'] = meters_to_miles(dict1['length_3d'])

    dict1['uphill_feet'] = meters_to_feet(dict1['uphill'])
    dict1['downhill_feet'] = meters_to_feet(dict1['downhill'])

    dict1['moving_time_HMS'] = convert_HMS(dict1['moving_time'])
    dict1['moving_distance_miles'] = meters_to_miles(dict1['moving_distance_meters'])

    dict1['stopped_time_HMS'] = convert_HMS(dict1['stopped_time'])
    dict1['stopped_distance_miles'] = meters_to_miles(dict1['stopped_distance_meters'])

    if dict1['uphill'] > dict1['downhill']:
        dict1['ascent'] = True
        dict1['descent'] = False
    else:
        dict1['ascent'] = False
        dict1['descent'] = True

    if dict1['points_no'] > 0:
        distances = []
        previous_point = None
        for point in gpx_part.walk(only_points=True):
            if previous_point:
                distance = point.distance_2d(previous_point)
                distances.append(distance)
            previous_point = point
        dict1['points_distance'] = sum(distances) / len(list(gpx_part.walk()))
    #point dictionary creation for each segment
    point_dict = {}
    for point in gpx_part.points:
        point_dict[point.time] = {}
        point_dict[point.time]['latitude'] = point.latitude
        point_dict[point.time]['longitude'] = point.longitude
        point_dict[point.time]['elevation'] = point.elevation
        point_dict[point.time]['delta'] = point.time - dict1['start_time']
        point_dict[point.time]['elevation_feet'] = meters_to_feet(point.elevation)
    dict1['data_points'] = point_dict
    first_point = list(sorted(point_dict.keys()))[0]
    #below adds elevation delta to dictionary from start of segment
    for point in point_dict:
        point_dict[point]['elevation_delta'] = point_dict[point]['elevation'] - point_dict[first_point]['elevation']
        #point_dict[point]['elevation_delta_feet'] = point_dict[point]['elevation_feet'] - point_dict[first_point]['elevation_feet']
        #print(point_dict[point])

    return dict1

def run(gpx_files):
    master_dict = {}
    if not gpx_files:
        print('No GPX files given')
        mod_sys.exit(1)

    for gpx_file in gpx_files:
        try:
            gpx = mod_gpxpy.parse(open(gpx_file))
            dict1 = print_gpx_info(gpx, gpx_file)
            key1 = dict1['start_time'] #sets key to be the start time for each GPX file
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
