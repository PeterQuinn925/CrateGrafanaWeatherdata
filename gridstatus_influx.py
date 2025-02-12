import datetime
import time
import json
from influxdb import InfluxDBClient
import pandas
import gridstatus
INFLUXDB_ADDRESS = '127.0.0.1'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'weather'
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
influxdb_client.switch_database(INFLUXDB_DATABASE)
caiso = gridstatus.CAISO()
while True:
   result = caiso.get_fuel_mix("latest")
   fields = {}
   total = 0
   for col in result:
#       print(col," ",result[col][0])
       if "Interval" not in col:
           if "Time" in col:
               ts = result[col][0]
           else:
               fields[col]=result[col][0]
#               print(fields[col])
               total = total + fields[col]
   fields["Total"] = total
   #print (ts)
   print (fields)
   tags = {'foo':'none'}
   influx_msg = [{'measurement': 'electricity','fields':fields, 'name':'observation', 'tags':tags,'time':ts}]
   try:
      influxdb_client.write_points(influx_msg,batch_size=1000,time_precision='s')
   except Exception as e:
       print("******Error:",influx_msg)
       print (e)
   print (ts)
   time.sleep(60*5)
