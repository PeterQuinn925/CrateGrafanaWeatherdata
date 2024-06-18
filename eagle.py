#!/usr/bin/env python3
import requests
import xml.etree.ElementTree as ET
import datetime
import time
import json
from datetime import datetime
from influxdb import InfluxDBClient
INFLUXDB_ADDRESS = '127.0.0.1'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'weather'
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
influxdb_client.switch_database(INFLUXDB_DATABASE)


rate = 0.53406 #Tier 2 rate per kWh
url = "http://10.0.0.8/cgi-bin/post_manager/"
creds = ('00bxxx','ef1f2bd0xxxxxxxx') #cloudid, installid
head= {"Content-Type":"text/xml","Content-Lenght":"255"}

while True:

    command = "<Command><Name>device_query</Name><DeviceDetails><HardwareAddress>0x001350010016d90c</HardwareAddress>" \
    + "</DeviceDetails><Components><Component><Name>Main</Name><Variables>" \
    + "<Variable><Name>zigbee:InstantaneousDemand</Name></Variable>" \
    + "</Variables></Component></Components></Command>"

    #command = "<Command><Name>device_query</Name><DeviceDetails><HardwareAddress>0x001350010016d90c</HardwareAddress>" \
    #+ "</DeviceDetails><Components><All>Y</All></Components></Command>"

    response = requests.post(url,headers = head, auth=creds, data =command)

    root = ET.fromstring(response.text)
    useage = root[1][0][6][0]
    #print (useage[0].text, useage[1].text)
    use = float(useage[1].text)
    cost = use * rate/60 # cost per minute 
    #print (cost)

    command = "<Command><Name>device_query</Name><DeviceDetails><HardwareAddress>0x001350010016d90c</HardwareAddress>" \
    + "</DeviceDetails><Components><Component><Name>Main</Name><Variables>" \
    + "<Variable><Name>zigbee:CurrentSummationDelivered</Name></Variable>" \
    + "</Variables></Component></Components></Command>"

    response = requests.post(url,headers = head, auth=creds, data =command)

    root = ET.fromstring(response.text)
    summation = float(root[1][0][6][0][1].text)
    #print (useage[0].text, useage[1].text)
    dict1 = {}
    dict1['instantuse'] = use
    dict1['cost'] = cost
    dict1['currentsum'] = summation
    fields = json.dumps(dict1)

    print (fields)

    ts =  int(datetime.now().timestamp())
    tags = {'foo':'none'}
    influx_msg = [{'measurement': 'electricuseage','fields':dict1, 'name':'observation', 'tags':tags,'time':ts}]
    try:
       influxdb_client.write_points(influx_msg,batch_size=1000,time_precision='s')
    except:
       print("******Error:",influx_msg)
    print (ts)
    time.sleep(60)
