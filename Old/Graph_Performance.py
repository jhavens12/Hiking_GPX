import data_collect
import glob
import matplotlib.pyplot as plt
import pylab
import numpy as np
from pprint import pprint
import itertools

#Graphs a dynamic number of GPX files (ascents) based on seconds elapsed and elevation

file_list = glob.glob("/Users/Havens/Dropbox/PYTHON/Hiking2/GPX/*")

master_dict = data_collect.run(file_list)


graph_dictionary = {}
graph_titles = {}
for item,x in enumerate(master_dict):
    x_list = []
    y_list = []
    count = item+1

    #for x in master_dict: #for each hike (main gps file)
    graph_titles[count] = {}
    graph_titles[count] = master_dict[x]['ascent']['name']
    for y in master_dict[x]['ascent']['data_points']: #for each datapoint in first segment
        val = master_dict[x]['ascent']['data_points'][y]['delta']
        x_list.append(val.seconds)
        y_list.append(master_dict[x]['ascent']['data_points'][y]['elevation'])
    graph_dictionary[count] = {}
    graph_dictionary[count]['x']=x_list
    graph_dictionary[count]['y']=y_list

colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'])

plt.style.use('dark_background')
plt.rcParams['lines.linewidth'] = 2
for set,label in zip(graph_dictionary,graph_titles):
    plt.plot(graph_dictionary[set]['x'],graph_dictionary[set]['y'],label=graph_titles[label],color=next(colors))

plt.title('Rate vs Elevation')
plt.xlabel("Seconds Passed From Start")
plt.ylabel("Elevation (Meters)")

plt.legend()
plt.show()
