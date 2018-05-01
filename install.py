#!/usr/bin/env python
import sys
import subprocess
from os.path import expanduser

subprocess.call(["sudo","cp", ".conkyrc_departure_monitor",expanduser("~")+"/.conkyrc_departure_monitor"])
subprocess.call(["sudo","cp", "efaconky","/usr/bin/efaconky"])
subprocess.call(["sudo","chmod","777","/usr/bin/efaconky"])
subprocess.call(["mkdir",expanduser("~")+"/.efaconky"])
subprocess.call(["mkdir",expanduser("~")+"/.efaconky/db"])
subprocess.call(["sudo","cp","-r", "src",expanduser("~")+"/.efaconky"])
subprocess.call(["sudo","chmod", "-R","777",expanduser("~")+"/.efaconky/src"])
if len(sys.argv) > 1:
    if sys.argv[1] == "all":
        subprocess.call(["sudo","apt-get","install","conky"])
        subprocess.call(["sudo","apt-get","install","net-tools"])
        subprocess.call(["pip","install","conkyutil"])
        subprocess.call(["pip","install","tinydb"])
        subprocess.call(["pip","install","netifaces"])
        subprocess.call(["pip","install","lxml"])
print "Install complete"
print "You can now remove this directory"
print "Use 'efaconky' to start"
