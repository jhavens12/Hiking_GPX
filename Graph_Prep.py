import data_collect_prep as data_collect
import glob
import matplotlib.pyplot as plt
import pylab
import numpy as np
from pprint import pprint
import itertools
import numpy

# 145: {'distance_from_previous': 12.519270330907082,
#  'distance_from_start': 3620.672758173153,
#distance_from_start_miles
# distance_from_start_feet
#  'elevation': 1237.523,
#  'elevation_delta': 686.492,
#  'elevation_delta_feet': 2250.66,
#  'elevation_feet': 4058.4,
#  'latitude': 44.31952499784529,
#  'longitude': -72.88638004101813,
#  'time': None,
#  'time_delta': 0,
#  'time_delta_seconds': 0}},
#time_delta_minutes

#graph_x = 'time_delta_minutes'
graph_x = 'distance_from_start_miles'
graph_y = 'elevation_delta_feet'
#graph_y = 'elevation_feet'

file_list = glob.glob("/Users/Havens/Dropbox/PYTHON/Hiking_Full/GPX_Tracks/*")

master_dict = data_collect.run(file_list)

#pprint(master_dict)

graph_dictionary = {}
graph_titles = {}
for item,x in enumerate(master_dict):
    x_list = []
    y_list = []
    count = item+1

    for set,gpx_part in enumerate(master_dict[x]['segments']):
        loop_count = set+1
        run_through = str(count)+"."+str(loop_count)
        run_through_list_x = []
        run_through_list_y = []
        graph_titles[run_through] = {}
        graph_titles[run_through] = master_dict[x]['segments'][gpx_part]['name']
        print(master_dict[x]['segments'][gpx_part]['name'])
        for y in master_dict[x]['segments'][gpx_part]['data_points']: #for each datapoint in first segment
            run_through_list_x.append(master_dict[x]['segments'][gpx_part]['data_points'][y][graph_x])
            run_through_list_y.append(master_dict[x]['segments'][gpx_part]['data_points'][y][graph_y])
        if sum(run_through_list_x) != 0 and sum(run_through_list_y) != 0:
            graph_dictionary[run_through] = {}
            graph_dictionary[run_through]['x']=run_through_list_x
            graph_dictionary[run_through]['y']=run_through_list_y
        else:
            print(master_dict[x]['segments'][gpx_part]['name'],"Issue with data - something equals 0")

#pprint (graph_dictionary)
colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])


#plt.style.use('dark_background')
plt.rcParams['lines.linewidth'] = 2
for set,label in zip(graph_dictionary,graph_titles):
    plt.plot(graph_dictionary[set]['x'],graph_dictionary[set]['y'],label=graph_titles[label],color=next(colors))
plt.title(str(graph_x)+" vs "+str(graph_y))
plt.xlabel(graph_x)
plt.ylabel(graph_y)
plt.legend()
#fig = plt.figure()
#ax = plt.gca()
#ax.set_yticks(numpy.arange(0, 5000, 500))
#ax.set_xticks(numpy.arange(0, 135, 15))
plt.grid(True)
#plt.rc('grid', linestyle=".", color='black')


#plt.title("test")
plt.show()
