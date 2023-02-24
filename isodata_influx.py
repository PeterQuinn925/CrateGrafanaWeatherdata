#comment out the sre_parse import in the caiso.py
#https://pypi.org/project/isodata/#getting-started
import isodata
import datetime
import time
import json
from influxdb import InfluxDBClient
import pandas

INFLUXDB_ADDRESS = '127.0.0.1'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'weather'
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
influxdb_client.switch_database(INFLUXDB_DATABASE)

iso = isodata.get_iso('caiso')
caiso = iso()
i = 1
max = 10000 #debugging
while i < max:
   result = caiso.get_latest_fuel_mix()
   fields = {}
   for fuel in result.mix.T:
        fields[fuel] = result.mix.at[fuel,'MW']
        if  pandas.isnull(fields[fuel]) : fields[fuel]=0
   ts =  result.time.to_pydatetime()
   print (ts)
   print (fields)
   tags = {'foo':'none'}
   influx_msg = [{'measurement': 'electricity','fields':fields, 'name':'observation', 'tags':tags,'time':ts}]
   try:
      influxdb_client.write_points(influx_msg,batch_size=1000,time_precision='s')
   except:
      print("******Error:",influx_msg)
   time.sleep(60*5)
