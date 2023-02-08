from mqttclient import MQTTClient
from math import sin
import network
import sys

from ina219 import INA219
from machine import I2C, Pin
from board import SDA, SCL
import time
import logging


"""
Send measurement results from microphyton board to host computer.
Use in combination with mqtt_plot_host.py.

'print' statements throughout the code are for testing and can be removed once
verification is complete.
"""

# Important: change the line below to a unique string,
# e.g. your name & make corresponding change in mqtt_plot_host.py

i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

print("scanning I2C bus ...")
print("I2C:", i2c.scan())

SHUNT_RESISTOR_OHMS = 0.1
ina = INA219(SHUNT_RESISTOR_OHMS, i2c)
ina.configure()


session = "kevinw"
BROKER = "mqtt.thingspeak.com"

# check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
	print("no wifi connection")
	sys.exit()
else:
	print("connected to WiFi at IP", ip)

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(BROKER, port='1883')
print("Connected!")

#topic = 'channels/1316473/publish/8ZU9D21U6HBNB4DU'
topic = 'channels/1334113/publish/T2S5LSWNYOZ9GNDG'

# topicData = "{}/data".format(session)
# topicPlot = "{}/plot".format(session)

# send data
# In this sample, we send "fake" data. Replace this code to send useful data,
# e.g. measurement results.
for t in range(100):
	I = ina.current()
	V = ina.voltage()
	P = I*V
	if I == 0:
		R = 0
	else:
		R = V/I*1000

	data="field1={}&field2={}".format(V,I)
	print(data)
	mqtt.publish(topic, data)
	time.sleep(15)


# # do the plotting (on host)
# print("tell host to do the plotting ...")
# mqtt.publish("{}/plot".format(session), "create the plot")

# free up resources
# alternatively reset the microphyton board before executing this program again
mqtt.disconnect()
