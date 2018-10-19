#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19
# @Author  : Anchor
# @File    : ONSUtil.py
# @Des     : 阿里ONS测试工具类

import hmac
import base64
from hashlib import sha1
import time
from paho.mqtt.client import MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING, MQTT_LOG_ERR, MQTT_LOG_DEBUG
from paho.mqtt import client as mqtt


#accessKey get from aliyun account console
accessKey = 'XXXXXX'
#secretKey get from aliyun account console
secretKey = 'XXXXX'
#MQTT GroupID,get from mq console
groupId = 'GID_XXX'
client_id=groupId+'@@@'+'TEST00001'
# Topic
topic = 'XXXX/python/test'
#MQTT endPoint get from mq console
brokerUrl='XXXXXXXXX'
def on_log(client, userdata, level, buf):
    if level == MQTT_LOG_INFO:
        head = 'INFO'
    elif level == MQTT_LOG_NOTICE:
        head = 'NOTICE'
    elif level == MQTT_LOG_WARNING:
        head = 'WARN'
    elif level == MQTT_LOG_ERR:
        head = 'ERR'
    elif level == MQTT_LOG_DEBUG:
        head = 'DEBUG'
    else:
        head = level
    print('%s: %s' % (head, buf))
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected disconnection %s' % rc)



client = mqtt.Client(client_id, protocol=mqtt.MQTTv311, clean_session=True)
client.on_log = on_log
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
password = base64.b64encode(hmac.new(secretKey.encode(), groupId.encode(), sha1).digest()).decode()
client.username_pw_set(accessKey, password)
client.connect(brokerUrl, 1883, 60)
client.subscribe(topic, 0)
for i in range(1, 11):
    print(i)
    rc = client.publish(topic, str(i), qos=0)
    print ('rc: %s' % rc)
    time.sleep(0.1)
client.loop_forever()