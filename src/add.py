#!/usr/bin/env python
from subprocess import Popen, PIPE
from tinydb import TinyDB, Query
from getRouterMacAdress import *
import re, os

try:
    router_mac = getRouterMacAdress()
    station_id = str(input("Station_ID:"))
    if os.path.dirname(__file__) is not '':
        db = TinyDB(os.path.dirname(__file__)+'/../db/db.json')
    else:
        db = TinyDB('../db/db.json')
    db.insert({'Station': station_id, 'MAC': router_mac})
    print "Done!"
except Exception, exc:
    print "Something went wrong!"
    print exc
