import paho.mqtt.client as mqtt
import serial
import time
import string
import paho.mqtt.publish as publish
import time

# Configure the MQTT broker and topic
mqtt_broker = "54.252.174.24"
mqtt_port = 1883
mqtt_topic = "temperature_data"

# Configure the Bluetooth communication (you need to install necessary libraries)
# For Bluetooth communication, you can use a library like PyBluez.

ser = serial.Serial("/dev/rfcomm0", 9600)
ser.write(str.encode('Start\r\n'))


def on_message(client, userdata, message):
    # Callback when a message is received from Teensy
    data = message.payload.decode()
    print(data)
    # Publish the received data to MQTT
    #mqtt_client.publish(mqtt_topic, data)

def on_connection(client,udata,flags,rc):
	print("Connection done")
	mqtt_client.subscribe(mqtt_topic)
	

# Configure the MQTT client
mqtt_client = mqtt.Client()

try:
	mqtt_client.on_message = on_message
	mqtt_client.on_connect = on_connection
	mqtt_client.connect(mqtt_broker, mqtt_port)
	mqtt_client.loop_start()
	print(ser)
	while True:
		if ser.in_waiting > 0:
			d_val=ser.readline().decode('utf-8')
			print(d_val ,end='\n')
			publish.single(mqtt_topic, d_val, hostname=mqtt_broker)
			time.sleep(2)

	
except:
	print("Adios!!")
# Main loop to receive data from Bluetooth and publish to MQTT
#mqtt_client.loop_forever()
