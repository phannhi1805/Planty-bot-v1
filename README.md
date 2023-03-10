# Planty-bot-v1

Project Logic 

Sensor: moisture sensor, ultrasonic sensor
Actuator: motor turned into a mini water pump

Logic: The moisture sensor is put in the soil for 24/7. Every 6 hours, it would measure the moisture content in the soil. If the output value is higher than a designated threshold value which is currently set as 2500 (for preference, calibration for air is ~2850 and for water is ~1450), it would print the phrase “Soil is dry, watering” and set the relay value to 0, which allows the power to go throw hence activates the water pump for 5 seconds. There is a pipe connecting from the pump and fixed on the pot so that no water is spilled in the process. After 5 seconds, it would print out the phrase “Plant is watered”. Each cycle is paused for 6 hours (21600 seconds) to ensure that the plant is water properly if the moisture sensor reads barely several units below the threshold. After 6 hours, the cycle would repeat as above, but if the moisture sensor output value is lower than the threshold value, it would just print out “Soil is still wet, no need for watering” and terminate the cycle. 
After every watering, the ultrasonic sensor would measure the distance from the water level and do calculations with the hardcoded container height (which is 8cm for my case) to produce the percentage of water left in the container. These values are sent to the Adafruit MQTT and connected to the IFTTT. If the percent water is lower than 20%, it would trigger the IFTTT to send a notification to the user’s phone.

Improvement 
	•	Use AA or AAA instead of lithium battery so it’s more universal.
	
	•	Set up multiple water pumps and moisture sensors so it can water different plants at a time. 
	
	•	Have the system play a sound after every watering (maybe just a joyful sound like Japanese rice cookers when they finish cooking or an announcement of what plant was watered). I would implement this but it would be bothersome if the sound goes off in the middle of the night. Need some way to stop the sound, or even the watering, form 10pm to 8pm or so. 
	
	•	Have it completely operate on the wifi and a power source instead of connecting to the computer. 
	
	•	Be able to take user input of container height and pot size so the system is more versatile. Not sure how to do so unless I make an actual app. Right now the system only caters toward my needs. 


Demo video: https://drive.google.com/file/d/1_IuZ2bsEU5WOw0cmzjz_r5W-pmZZtC3g/view
