from pprint import pprint
import glob
import data_collect_prep as data_collect
from pprint import pprint

#used on groups of GPX files aka ascents.gpx


file_list = glob.glob("/Users/Havens/Dropbox/PYTHON/Hiking_full/GPX_Tracks/*")

master_dict = data_collect.run(file_list)
#pprint(master_dict)

print ("Hike Information:")

for x in master_dict:
    print (master_dict[x]['file'])
    print ("Moving Time: ",master_dict[x]['moving_time_HMS'])
    print ("Stopped Time: ",master_dict[x]['stopped_time_HMS'])
    #print ("Total Time: ",master_dict[x]['total_time'])
    print ("Moving Distance (Miles): ",master_dict[x]['moving_distance_miles'])
    print ("Uphill Feet: ",master_dict[x]['uphill_feet'])
    print ("Downhill Feet: ",master_dict[x]['downhill_feet'])
    for y in master_dict[x]['segments']:
        print ("    Ascent: ")
        print ("        Moving Time: ",master_dict[x][y]['moving_time_HMS'])
        print ("        Stopped Time: ",master_dict[x][y]['stopped_time_HMS'])
        print ("        Moving Distance (Miles): ",master_dict[x][y]['moving_distance_miles'])
        print ("        Uphill Feet: ",master_dict[x][y]['uphill_feet'])
        print ()
