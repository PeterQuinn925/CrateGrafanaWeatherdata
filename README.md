# CrateGrafanaWeatherdata
Extract data from Weewx and post via MQTT to Cratedb and view with Grafana

mqtt_weather.py runs on Raspi 3 that contains Weewx. Weewx updates the SQLite db every 2 minutes with new data. This code reads the latest and posts it to MQTT topic Weather/data

Install mosquitto and mosquitto-clients using sudo apt install
   sudo nano /etc/mosquitto/mosquitto.conf
add at the bottom:
   listener 1883
   allow_anonymous true
and restart mosquitto

mqtt_subscribe runs on Raspi 4 and subscribes to the weather data topic. When complete, it will post the messages to InfluxDB

Mosquitto is running on Raspi4, but it could be elsewhere.
