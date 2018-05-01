from subprocess import Popen, PIPE
import netifaces as ni
import re
# Small Skript to get Mac Adress of Router under Unix
# Dependencies: net-tool (sudo apt-get install net-tool)
#               netifaces (pip install netifaces)
def getRouterMacAdress():
    IP = gws= ni.gateways()['default'][ni.AF_INET][0]
    pid = Popen(["arp", "-n", IP], stdout=PIPE)
    s = pid.communicate()[0]
    mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]
    return mac
