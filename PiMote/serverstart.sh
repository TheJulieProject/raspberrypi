#!/bin/sh
cd mjpg-streamer/mjpg-streamer
./start.sh&
cd ../..
python $1.py 0.0.0.0 8090
