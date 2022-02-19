
import datetime
import time
import paho.mqtt.client as mqttClient
import json

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
#    print("message qos=",message.qos)
#    print("message retain flag=",message.retain)

Connected = False
broker_address= "localhost"
port = 1883
topic = "weather/data"
client = mqttClient.Client("Raspi4")
client.on_message=on_message
client.connect(broker_address,port=port)
#client.loop_forever()
client.subscribe(topic)
client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)

