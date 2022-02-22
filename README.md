# CrateGrafanaWeatherdata

Extract data from Weewx and post via MQTT to InfluxDB (not Cratedb) and view with Grafana
I wanted to use Crate, but it was too difficult to get it going on a single Raspberry Pi, so I refocused on InfluxDB instead.

**mqtt_weather.py/** 
Runs on Raspi 3 that contains Weewx. Weewx updates the SQLite db every 2 minutes with new data. This code reads the latest and posts it to MQTT topic Weather/data. The script mqtt_weather is the script that goes in /etc/init.d for the daemon. See http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/

Install mosquitto and mosquitto-clients using sudo apt install
   sudo nano /etc/mosquitto/mosquitto.conf
add at the bottom:
   listener 1883
   allow_anonymous true
and restart mosquitto

**mqtt_subscribe/**
Runs on Raspi 4 and subscribes to the weather data topic. It then posts the messages to InfluxDB

Mosquitto is running on Raspi4, but it could be elsewhere.

Install Grafana and connect it to the Influx instance on Raspi4. Use topic 'weather'
![image](https://user-images.githubusercontent.com/18488357/155051595-25dd9737-9b3a-451d-9fba-27756b9b2cdb.png)
