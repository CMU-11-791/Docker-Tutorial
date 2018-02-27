#!/usr/bin/env bash

python stop.py
sleep 2
docker rm $(docker ps -q -f "status=exited")
