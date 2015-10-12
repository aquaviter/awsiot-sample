#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as paho
import ssl
from functools import wraps
import json
import time
import random

mytopic = 'device/sensor'

def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1_2
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)

mqttc = paho.Client()
mqttc.tls_set("./rootca.pem",
               "./cert.pem",
               "./privatekey.pem")
mqttc.connect("data.iot.us-east-1.amazonaws.com", 8883, 10)

while True:
    timestamp = int(time.time())
    value = random.randint(100,150)
    record = {
        "timestamp": timestamp,
        "value": value
    }
    message = json.dumps(record)
    print message
    mqttc.publish(mytopic, message, 0, False)
    time.sleep(1)
