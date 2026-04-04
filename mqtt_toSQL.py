#!/usr/bin/python3
import datetime
import time
import paho.mqtt.client as mqttClient
import json
import sqlite3
import os

# old location DATABASE = '/home/ubuntu/location.db'
DATABASE = '/var/lib/grafana/data/location.db'

def on_message(client, userdata, message):
   global cursor, conn
   mqtt_msg = json.loads(message.payload)
   print (mqtt_msg)
   try:
      insert_SQL = 'INSERT INTO location(ts,lat,lng) VALUES(?,?,?)'
      cursor.execute(insert_SQL, (mqtt_msg["time"], mqtt_msg["lat"], mqtt_msg["lng"]))
      conn.commit()
      print("row committed")
   except Exception as e:
      print("Error:", e)

#create SQlite db and tables if they don't exist
create_table = """CREATE TABLE IF NOT EXISTS location (
    ts INTEGER PRIMARY KEY,
    lat FLOAT,
    lng FLOAT);"""
try:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(create_table)
        conn.commit()

except sqlite3.OperationalError as e:
    print(e)

Connected = False
broker_address= "localhost"
port = 1883
topic = "location/test"
clientname= "OC_" + str(os.getpid()) #to make sure it's unique when it restarts
client = mqttClient.Client(clientname)
client.on_message=on_message
client.connect(broker_address,port=port)
#client.loop_forever()
client.subscribe(topic)
client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)
