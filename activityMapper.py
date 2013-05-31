#!/usr/bin/python
# TODO: 2013-05-07-1215.gpx is malformed, premature </trkseg> closure, try catch to ignore

import pygmaps
import zipfile
import re
import argparse
from xml.dom import minidom

RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000FF"

def activity_color(activity_type):
	if activity_type == "Cycling":
		return RED
	elif activity_type == "Walking":
		return GREEN
	else:
		return BLUE

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="file containing your activities")
args = parser.parse_args()

# TODO: Figure out what the center should be
mymap = pygmaps.maps(40.645, -111.933, 16)

with zipfile.ZipFile(args.i, "r") as zfile:
    for name in zfile.namelist():
	if not name.endswith(".gpx"):
		continue

	path = []

	# TODO: Setup layers for each activity type
	# TODO: Take flag from user input to only map certain activity types
	xmldoc = minidom.parse(zfile.open(name))
	itemlist = xmldoc.getElementsByTagName('trkpt')
	
	activityName = xmldoc.getElementsByTagName('name')[0].firstChild.nodeValue
	activityType = re.search(r'^([\w]+)', activityName).group()
	print "Processing %s (%s)" % (name, activityType)
	
	#TODO: De-duplication, keep track of last coords and if they're the same don't add them again
	for s in itemlist :
	    path.append([float(s.attributes['lat'].value), float(s.attributes['lon'].value)])
	
	mymap.addpath(path, activity_color(activityType))

print "Generating map..."
mymap.draw('./activityMap.html')
