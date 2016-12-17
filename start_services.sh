#!/usr/bash

python Myservice.py
python Myworker.py
tail -100f ./conf/server.conf