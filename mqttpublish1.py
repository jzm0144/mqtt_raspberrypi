import paho.mqtt.client as mqtt
from random import randrange, uniform
import numpy as np
import time, struct
from datetime import datetime
import ipdb as ipdb
import json


# config.json file contains the configurations for the mqtt publisher/listener scripts
# to change the configurations, edit the the key, val pairs in config.json
with open('config.json') as config_file:
    data = json.load(config_file)

unit_id = data['unit_id']
mqtt_publish_sec = data['mqtt_publish_sec']
topic = data['topic']
mqttBroker = data['mqttBroker']
client_id = data['client']

print("Unit ID:          ", unit_id)
print("Publish Interval: ", mqtt_publish_sec)
print("Topic:            ", topic)
print("Broker:           ", mqttBroker)
print("Client:           ", client_id)


mqttBroker = mqttBroker

client = mqtt.Client(client_id)
client.connect(mqttBroker)

msgcounter = 0
while True:

    # Synthesize some sample data - a time and 24 floats 0..700
    payload = [unit_id] + [time.time()] + [round(uniform(0, 700), 3)  for _ in range(24)]
    # Pack as 25 IEEE754 floats of 4 bytes each
    payload = struct.pack('!26d', *payload)
    
    client.publish(topic, payload)
    msgcounter += 1
    print(msgcounter, "  Just published from ", client_id, " to Topic = ", topic,"  payload: ", len(payload), " Bytes")
    time.sleep(10)
