#!/usr/bin/env python
from xml.etree import ElementTree as ET
from subprocess import Popen, PIPE
from tinydb import TinyDB, Query
from conkyutil.writer import ConkyWriter
from os.path import expanduser
from getRouterMacAdress import *
import urllib2
import re, os
import signal

def handler(signum, frame):
    """Handler for function timeout"""
    print "REQUEST TIMED OUT :("
    raise Exception("")

def departure_monitor(station):
    """Returns departure monitor information by station ID"""
    output = []
    signal.alarm(30)
    try:
        # First request to get session ID
        response = urllib2.urlopen('http://www.efa-bw.de/nvbw/XML_DM_REQUEST?sessionID=0&type_dm=any&name_dm='+str(station)+'&itdDateTimeArr=dep')
        xml = response.read()
        tree = ET.fromstring(xml)
        sid = tree.get('sessionID') #sessionID to get departure Data
        # Secound Request to get monitor data
        response2 = urllib2.urlopen('http://www.efa-bw.de/nvbw/XML_DM_REQUEST?sessionID='+sid+'&requestID=1&dmLineSelectionAll=1')
        xml2 = response2.read()
        departures_tree = ET.fromstring(xml2)
        hours = departures_tree.find('itdDepartureMonitorRequest').find('itdDateTime').find('itdTime').get('hour')
        if int(hours) < 10:
            hours = '0'+hours
        minutes = departures_tree.find('itdDepartureMonitorRequest').find('itdDateTime').find('itdTime').get('minute')
        if int(minutes) < 10:
            minutes = '0'+minutes
        time = hours+':'+minutes
        station_name = departures_tree.find('itdDepartureMonitorRequest').find('itdOdv').find('itdOdvName').find('odvNameElem').text
        if station_name is None:
            station_name = departures_tree.find('itdDepartureMonitorRequest').find('itdOdv').find('itdOdvName').find('odvNameInput').text
        output.append("${font}${font Poiret One:size=15}"+station_name.encode("UTF8")+"${font}${font DejaVu Sans Mono:size=10}")
        # count init
        count = 1
        for itdDeparture in departures_tree.find('itdDepartureMonitorRequest').find('itdDepartureList'):
            abfahrt_class = ""
            abfahrt = itdDeparture.get('countdown')
            line = itdDeparture.find('itdServingLine').get('number')
            destination = itdDeparture.find('itdServingLine').get('direction')
            # Break if 5 entries written
            if int(abfahrt) > 30 or count > 15:
                break
            dest_offset = 30
            # Correct if german "Umlaute" appear in Station Name
            if u"\u00FC" in destination or u"\u00E4" in destination or u"\u00F6" in destination or u"\u00DF" in destination:
                dest_offset += 1
            if int(abfahrt)-1 >= 0:
                count += 1
                output.append("\\- " + '{:<4}'.format(line[:3])  +" "+ ('{:<'+str(dest_offset)+'}').format(destination.encode("UTF8")) +" "+'{:>3}'.format(str(int(abfahrt)-1)))
    except Exception, exc:
        print "Something went wrong!"
        print exc

    return output

def get_station_db():
    """Returns all station IDs linked to network"""
    try:
        router_mac = getRouterMacAdress()
        if os.path.dirname(__file__) is not '':
            db = TinyDB(os.path.dirname(__file__)+'/../db/db.json')
        else:
            db = TinyDB('../db/db.json')
        station_query = Query()
        result = db.search((station_query.MAC == router_mac))
        stationlist = []
        for item in result:
            stationlist.append(item['Station'])
        return stationlist
    except:
        return []

# Init Timout signal
signal.signal(signal.SIGALRM, handler)

# Get requested station IDs from Database
station_ids = get_station_db()

# Get Stationdata
printout = []
for item in station_ids:
    printout += departure_monitor(item)

# Open output Stream
writer = ConkyWriter()

# Print every row with information from the station printout
for item in printout:
    writer.voffset(12).offset(12).color('white').write(item)
    writer.newline()

# Print two newlines to prevent content cutoff
writer.newline()
writer.newline()
