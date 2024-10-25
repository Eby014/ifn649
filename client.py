import paho.mqtt.client as mqtt
import serial
def on_connect(client, userdata, flags, rc):
	print("Connected to MQTT")
	print("Connection returned result: " + str(rc) )
	client.subscribe("ifn649")
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	ser = serial.Serial("/dev/rfcomm0", 9600)
	ser.write(msg.payload) # instead of “Start\r\n”, send the actual message.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("54.252.174.24", 1883, 60)
client.loop_forever()a
