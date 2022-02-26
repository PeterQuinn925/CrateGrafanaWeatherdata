#!/usr/bin/python3
import sqlite3
from sqlite3 import Error
import datetime
import time
import datetime
import json
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = '127.0.0.1'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'weather'
database = r"/home/pi/weewx.sdb"

conn = sqlite3.connect(database)

#querystring = "SELECT dateTime, barometer,inTemp,extraTemp2,outTemp,pm2_5,pm10_0 from archive where dateTime>1644172560"
querystring = "SELECT dateTime, barometer,inTemp,extraTemp2,outTemp,pm2_5,pm10_0 from archive where dateTime>?"
#2 years
#lasttime = 1387200000
#1 month
#lasttime = 1642903619
#forever
lasttime = 1000000000

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
influxdb_client.switch_database(INFLUXDB_DATABASE)


cur = conn.cursor()
column_name=[col[0] for col in cur]
cur.execute(querystring,(str(lasttime),))

rows = [ dict(line) for line in [zip([ column[0] for column in cur.description], row) for row in cur.fetchall()] ]
i=0
for row in rows:
   payload = row
   timestamp = payload["dateTime"]
#8 hours behind due to time zones, I think
#8hr*60min*60sec
   u_time = datetime.datetime.fromtimestamp(int(timestamp)+28800)
   f_time =u_time.strftime('%Y-%m-%dT%H:%M:%S') 
   del payload['dateTime']
   if payload['extraTemp2'] is not None and payload['extraTemp2']>100:
      payload['extraTemp2']=70
   tags = {'foo':'none'}
   influx_msg = [{'measurement': 'weather','fields':payload, 'name':'observation', 'tags':tags,'time':f_time}]
#      print (influx_msg)
   try:
      influxdb_client.write_points(influx_msg,batch_size=1000,time_precision='s')
   except:
      print("******Error:",influx_msg)
   if i % 10000 == 0:
      print (i)
      print (influx_msg)
   i=i+1



