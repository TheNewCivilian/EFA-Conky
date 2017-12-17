from subprocess import Popen, PIPE
from wireless import Wireless
from tinydb import TinyDB, Query
import netifaces
import re

try:
    router_mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", Popen(["arp", "-a"], stdout=PIPE).communicate()[0]).groups()[0]
    accept = raw_input("Delete all Station mapped to this Network?[y/n]:")
    wireless = Wireless()
    ss_id = wireless.current()
    db = TinyDB('../db/db.json')
    if accept is 'y':
        network_query = Query()
        result = db.search((network_query.SSID == ss_id)&(network_query.MAC == router_mac))
        for item in result:
            #print item.doc_id
            db.remove(doc_ids=[item.doc_id])
    print "Done!"
except Exception, exc:
    print "Something went wrong!"
    print exc
