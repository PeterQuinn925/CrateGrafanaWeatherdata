#!/usr/bin/env bash
set -e
cd /home/pi
source /home/pi/caiso-env/bin/activate
python3 /home/pi/caiso-env/gridstatus_influx.py
