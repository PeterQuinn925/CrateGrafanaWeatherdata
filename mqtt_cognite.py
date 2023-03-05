#!/usr/bin/python3
import datetime
import time
import paho.mqtt.client as mqttClient
import json
import os
from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.data_classes import TimeSeries

host = "https://az-eastus-1.cognitedata.com/"
myproject = "rockwell-demo"
tenant = "e2d0f0a5-fc45-414a-b012-0540e46a2d88"
clientid = "d9fbc603-0729-4f6b-ad18-33b084f06c45"
secret = "bogusbogusbogusbogusbogusbogus"
myscope = "https://az-eastus-1.cognitedata.com/.default"
token="https://login.microsoftonline.com/"+tenant+"/oauth2/v2.0/token"

creds = OAuthClientCredentials(token_url=token,client_id=clientid, client_secret=secret, scopes=myscope)
cnf = ClientConfig(client_name="pdq_home", base_url=host, project=myproject, credentials=creds)
c_client = CogniteClient(cnf)
#ts_list = client.time_series.list()
#print (ts_list)



def on_message(client, userdata, message):
#    print("message received " ,str(message.payload.decode("utf-8")))
#    print("message topic=",message.topic)
#    print("message qos=",message.qos)
#    print("message retain flag=",message.retain)
    mqtt_msg = json.loads(message.payload)
    timestamp = mqtt_msg["dateTime"]
    print (timestamp)
    del mqtt_msg['dateTime']
#    print (mqtt_msg)
    for item in mqtt_msg:
       print(item, mqtt_msg[item])
       #see if there is a cognite timeseries for this value
       res = c_client.time_series.search(name="pdq_"+item)
       if res[0].name=="pdq_"+item:
           print (res[0].id)
           ts = res[0]
       else:
           ts = c_client.time_series.create(TimeSeries(name="pdq_"+item))
       datapoint = [(timestamp*1000,mqtt_msg[item])]
       c_client.time_series.data.insert(datapoint, id = ts.id)

       
       

Connected = False
broker_address= "Raspi4"
port = 1883
topic = "weather/data"
clientname= "Farmer_" + str(os.getpid()) #to make sure it's unique when it restarts
client = mqttClient.Client(clientname)
client.on_message=on_message
client.connect(broker_address,port=port)
#client.loop_forever()
client.subscribe(topic)
client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)
