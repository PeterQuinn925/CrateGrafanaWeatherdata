#python3
#https://pypi.org/project/isodata/#getting-started
import isodata
import datetime
import time
import json
from influxdb import InfluxDBClient
import pandas
from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.data_classes import TimeSeries

INFLUXDB_ADDRESS = '127.0.0.1'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'weather'
influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
influxdb_client.switch_database(INFLUXDB_DATABASE)

#Cognite data part is no longer used. It still should work if you have proper credentials
host = "https://az-eastus-1.cognitedata.com/"
myproject = "rockwell-demo"
tenant = "e2d0f0a5-fc45-414a-b012-0540e46a2d88"
clientid = "d9fbc603-0729-4f6b-ad18-33b084f06c45"
secret = "bogusbogusbogusbogusbogusbogus"
myscope = "https://az-eastus-1.cognitedata.com/.default"
token="https://login.microsoftonline.com/"+tenant+"/oauth2/v2.0/token"
ts_prefix = 'caiso_'
creds = OAuthClientCredentials(token_url=token,client_id=clientid, client_secret=secret, scopes=myscope)
cnf = ClientConfig(client_name="pdq_home", base_url=host, project=myproject, credentials=creds)
c_client = CogniteClient(cnf)

iso = isodata.get_iso('caiso')
caiso = iso()
while True:
   result = caiso.get_latest_fuel_mix()
   fields = {}
   total = 0
   for fuel in result.mix.T:
        fields[fuel] = result.mix.at[fuel,'MW']
        if  pandas.isnull(fields[fuel]) : fields[fuel]=0
        total = total + fields[fuel]
   fields["Total"] = total
   ts =  result.time.to_pydatetime()
   tags = {'foo':'none'}
   influx_msg = [{'measurement': 'electricity','fields':fields, 'name':'observation', 'tags':tags,'time':ts}]
   try:
      influxdb_client.write_points(influx_msg,batch_size=1000,time_precision='s')
   except:
      print("******Error:",influx_msg)
   print (ts)
   for item in fields:
       #see if there is a cognite timeseries for this value
       res = c_client.time_series.search(name=ts_prefix+item)
       if len(res)>0 and res[0].name==ts_prefix+item:
           #print (res[0].id)
           tseries = res[0]
       else:
           tseries = c_client.time_series.create(TimeSeries(name=ts_prefix+item))
       datapoint = [(ts,fields[item])]
       c_client.time_series.data.insert(datapoint, id = tseries.id)

   time.sleep(60*5)
