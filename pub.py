import paho.mqtt.publish as publish

publish.single("ifn649","LED_ON",hostname="3.25.174.17")
print("Done")
