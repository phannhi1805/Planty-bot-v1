import machine, time, network, sys
from mqttclient import MQTTClient
from machine import Pin, ADC, DAC, I2C
from time import sleep
from hcsr04 import HCSR04


# Check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# Set up Adafruit connection
adafruitIoUrl = 'io.adafruit.com'
adafruitUsername = 'ptpn1805'
adafruitAioKey = 'aio_vVNQ10Nw8tSSBIXtxrpuw9tygYgS'

# Define callback function
def sub_cb(topic, msg):
    print((topic, msg))

# Connect to Adafruit server
print("Connecting to Adafruit")
mqtt = MQTTClient(adafruitIoUrl, port='1883', user=adafruitUsername, password=adafruitAioKey)
time.sleep(0.5)
print("Connected!")

# This will set the function sub_cb to be called when mqtt.check_msg() checks
# that there is a message pending
mqtt.set_callback(sub_cb)

# Send test message
feedName = "ptpn1805/feeds/auto-watering-system"
testMessage = "10"
# testMessage = "1"
mqtt.publish(feedName,testMessage)
print("Published {} to {}.".format(testMessage,feedName))

mqtt.subscribe(feedName)

# For one minute look for messages (e.g. from the Adafruit Toggle block) on your test feed:
for i in range(0, 60):
    mqtt.check_msg()
    time.sleep(1)
