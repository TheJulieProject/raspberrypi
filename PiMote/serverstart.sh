#!/bin/sh
cd mjpg-streamer/mjpg-streamer
./start.sh&
cd ../..
python regular.py 0.0.0.0 8090
