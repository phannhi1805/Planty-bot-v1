import machine, time, network, sys
from mqttclient import MQTTClient
from machine import Pin, ADC, DAC, I2C
from time import sleep
from hcsr04 import HCSR04

# Set up pins and parameters
sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)
relay = Pin(26, Pin.OUT)
ultrasensor = HCSR04(trigger_pin=22, echo_pin=23,echo_timeout_us=1000000)

controlled_dry = 2500
watered = False
containterHeight = 8

# Check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)
    sleep(3)

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
feedName = "ptpn1805/feeds/water-level"

# Circuit action
# Check again after 6 hours (21600 seconds)
while True:
    value = sensor.read()
    print(value)
    if value > controlled_dry:
        print("Soil is dry, watering")
        relay.value(0)
        sleep(5)
        watered = True
    
    relay.value(1)

    if watered == True:
        print("Plant is watered")
        try:
            distance = ultrasensor.distance_cm()
            print(distance)
        except KeyboardInterrupt:
            pass
        water = ((containterHeight - distance) / containterHeight) * 100
        waterPercentage ="{:.2f}".format(water)
        print(waterPercentage)
        testMessage = str(waterPercentage)
        mqtt.publish(feedName,testMessage)
        print("Published {} to {}.".format(testMessage,feedName))
        mqtt.subscribe(feedName)
        watered = False
        sleep(10)
    else:
        print("Soil is still wet, no need for watering")
        watered = False
        sleep(10)