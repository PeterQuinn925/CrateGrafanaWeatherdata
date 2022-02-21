#!/usr/bin/python3
import sqlite3
from sqlite3 import Error
import datetime
import time
import paho.mqtt.client as mqttClient
import json

Connected = False
broker_address= "10.0.0.11"
port = 1883
client = mqttClient.Client("weatherdata")
#client.connect(broker_address,port=port)

database = r"/var/lib/weewx/weewx.sdb"

try:
    conn = sqlite3.connect(database)
except Error as e:
    pass

#querystring = "SELECT dateTime, barometer,inTemp,extraTemp2,outTemp,pm2_5,pm10_0 from archive where dateTime>1644172560"
querystring = "SELECT dateTime, barometer,inTemp,extraTemp2,outTemp,pm2_5,pm10_0 from archive where dateTime>?"
lasttime = 1645235000

while True:
    cur = conn.cursor()
    column_name=[col[0] for col in cur]
    cur.execute(querystring,(str(lasttime),))
    try:
       row = [ dict(line) for line in [zip([ column[0] for column in cur.description], row) for row in cur.fetchall()] ]
       print ("------")
       payload = json.dumps(row[len(row)-1])
       print (payload)
       client.connect(broker_address,port=port,keepalive=30)
       client.publish("weather/data",payload)
       lasttime = (row[len(row)-1]["dateTime"])
       print (lasttime)
    except:
       print ("error")
    time.sleep(120)
   

