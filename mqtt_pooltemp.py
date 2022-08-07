#!/usr/bin/python3
import datetime
import time
import paho.mqtt.client as mqttClient
import json
from influxdb import InfluxDBClient
import os

INFLUXDB_ADDRESS = '127.0.0.1'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'weather'

def on_message(client, userdata, message):
#    print("message received " ,str(message.payload.decode("utf-8")))
#    print("message topic=",message.topic)
#    print("message qos=",message.qos)
#    print("message retain flag=",message.retain)
    mqtt_msg = json.loads(message.payload)
#    timestamp = mqtt_msg["dateTime"]
#    f_time = timestamp
#    u_time = datetime.datetime.fromtimestamp(int(timestamp))
#    f_time =u_time.strftime('%Y-%m-%dT%H:%M:%S')
#    del mqtt_msg['dateTime']
    tags = {'foo':'none'}
#    influx_msg = [{'fields':mqtt_msg, 'name':'observation', 'tags':tags,'timestamp':timestamp}]
    influx_msg = [{'measurement': 'weather','fields':mqtt_msg, 'name':'pooltemp', 'tags':tags}]
    influx_json = json.dumps(influx_msg)
    print (influx_msg)
    influxdb_client.write_points(influx_msg,time_precision='s')

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)
influxdb_client.switch_database(INFLUXDB_DATABASE)


Connected = False
broker_address= "localhost"
port = 1883
topic = "weather/pooltemp"
clientname= "Raspi4_" + str(os.getpid()) #to make sure it's unique when it restarts
client = mqttClient.Client(clientname)
client.on_message=on_message
client.connect(broker_address,port=port)
#client.loop_forever()
client.subscribe(topic)
client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)

