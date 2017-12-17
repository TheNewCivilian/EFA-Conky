from xml.etree import ElementTree as ET
from subprocess import Popen, PIPE
from wireless import Wireless
from tinydb import TinyDB, Query
from conkyutil.writer import ConkyWriter
from os.path import expanduser
import urllib2
import netifaces
import re, os


def departure_monitor(station):
    output = []
    try:
        response = urllib2.urlopen('http://www.efa-bw.de/nvbw/XML_DM_REQUEST?sessionID=0&type_dm=any&name_dm='+str(station)+'&itdDateTimeArr=dep')
        xml = response.read()
        tree = ET.fromstring(xml)
        sid = tree.get('sessionID') #sessionID to get departure Data
        #Secound Request
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
        #print station_name
        if station_name is None:
            station_name = departures_tree.find('itdDepartureMonitorRequest').find('itdOdv').find('itdOdvName').find('odvNameInput').text
        output.append("${font}${font Poiret One:size=15}"+station_name.encode("UTF8")+"${font}${font DejaVu Sans Mono:size=10}")
        #writer.voffset(50).offset(12).color('white').write().newline()

        count = 1
        #print departures_tree.find('itdDepartureMonitorRequest').find('itdDepartureList')

        for itdDeparture in departures_tree.find('itdDepartureMonitorRequest').find('itdDepartureList'):
            abfahrt_class = ""
            abfahrt = itdDeparture.get('countdown')
            line = itdDeparture.find('itdServingLine').get('number')
            destination = itdDeparture.find('itdServingLine').get('direction')
            count += 1
            if count > 6:
                break
            #writer.voffset(12).offset(12).color('white').write(line + " " + destination.encode("UTF8") + " " + abfahrt).newline()
            #Print Line just letters if string is longer than 3 symbols
            #count special characters in destination an add to printlengh
            output.append("\\- " + '{:<4}'.format(line[:4])  +" "+ '{:<30}'.format(destination.encode("UTF8")) +" "+'{:>3}'.format(abfahrt))
        if count < 5:
            output.append("\Does not support standard EFA!")

    except Exception, exc:
        print "Something went wrong!"
        print exc

    return output

def get_station_db():
    router_mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", Popen(["arp", "-a"], stdout=PIPE).communicate()[0]).groups()[0]
    wireless = Wireless()
    ss_id = wireless.current()
    if os.path.dirname(__file__) is not '':
        db = TinyDB(os.path.dirname(__file__)+'/../db/db.json')
    else:
        db = TinyDB('../db/db.json')
    station_query = Query()

    try:
        result = db.search((station_query.SSID == ss_id)&(station_query.MAC == router_mac))
        stationlist = []
        for item in result:
            stationlist.append(item['Station'])
        return stationlist
    except:
        return []

station_ids = get_station_db()
printout = []
for item in station_ids:
    printout += departure_monitor(item)
#print printout
writer = ConkyWriter()
#
# with open(expanduser("~")+"/.conky_departure_monitor","w+") as conkyrc:
#     conkyrc.write("conky.config = {background=true,double_buffer=true,no_buffers=true,imlib_cache_size=10,draw_shades=false,draw_outline=false,use_xft=true,xftalpha=1,font='Droid Sans:size=10',text_buffer_size=300,override_utf8_locale=true,gap_x=0,gap_y=0,alignment='middle_right',own_window=true,own_window_type='desktop',own_window_transparent=true,own_window_hints='undecorated,below,sticky,skip_taskbar,skip_pager',own_window_argb_visual=true,own_window_argb_value=0,}conky.text = [[ ${font Droid Sans:size=14}           << DEPARTURES >>${font}${font Poiret One:size=15}\n------------------------------------------")

#writer = ConkyWriter(open(expanduser("~")+"/.conky_departure_monitor","a"))
for item in printout:
    writer.voffset(12).offset(12).color('white').write(item)
    writer.newline()
writer.newline()
writer.newline()
#writer.voffset(12).offset(12).color('white').write("${font}]]")
