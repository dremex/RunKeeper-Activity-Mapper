#!/usr/bin/python

import pygmaps
import zipfile
import re
import argparse
import xml.parsers.expat
from xml.dom import minidom

RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000FF"
ORANGE = "#FF8C00"

def activity_color(activity_type):
	if activity_type == "Cycling":
		return RED
	elif activity_type == "Walking":
		return GREEN
	elif activity_type == "Running":
		return BLUE
	else:
		return ORANGE

parser = argparse.ArgumentParser()
parser.add_argument("-i", required=True, help="zip file containing your activities")
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
	try:
		xmldoc = minidom.parse(zfile.open(name))
	except xml.parsers.expat.ExpatError:
		print "---Error parsing file, skipping"
		continue
		
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
