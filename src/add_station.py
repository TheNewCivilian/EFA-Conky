
from subprocess import Popen, PIPE
from wireless import Wireless
from tinydb import TinyDB, Query
import netifaces
import re

try:
    router_mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", Popen(["arp", "-a"], stdout=PIPE).communicate()[0]).groups()[0]
    station_id = str(input("Station_ID:"))
    wireless = Wireless()
    ss_id = wireless.current()
    db = TinyDB('../db/db.json')
    db.insert({'Station': station_id, 'SSID': ss_id, 'MAC': router_mac})
    print "Done!"
except Exception, exc:
    print "Something went wrong!"
    print exc
