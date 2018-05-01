#!/usr/bin/env python
from subprocess import Popen, PIPE
from wireless import Wireless
from tinydb import TinyDB, Query
from getRouterMacAdress import *
import re, os

try:
    router_mac = getRouterMacAdress()
    accept = raw_input("Delete all Station mapped to this Network?[y/n]:")
    if os.path.dirname(__file__) is not '':
        db = TinyDB(os.path.dirname(__file__)+'/../db/db.json')
    else:
        db = TinyDB('../db/db.json')
    if accept is 'y':
        network_query = Query()
        result = db.search(network_query.MAC == router_mac)
        for item in result:
            #print item.doc_id
            db.remove(doc_ids=[item.doc_id])
    print "Done!"
except Exception, exc:
    print "Something went wrong!"
    print exc
