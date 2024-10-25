import paho.mqtt.client as mqtt

# Configure the MQTT broker and topic
mqtt_broker = "54.252.174.24"  # Replace with actual MQTT broker IP or hostname
mqtt_port = 1883
mqtt_topic = "temperature_data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker!")
        client.subscribe(mqtt_topic)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, message):
    # Callback when a message is received from Teensy
try:
        data = message.payload.decode()
        print(f'Received data: {data}')
        # You can process the received data as needed
    except Exception as e:
        print(f"Error processing message: {e}")

# Configure the MQTT client
mqtt_client = mqtt.Client()

# Assign the on_connect and on_message callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
try:
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    print("Connecting to broker...")
except Exception as e:
    print(f"Failed to connect to broker: {e}")

# Start the MQTT client loop to receive data
try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("MQTT client loop stopped.")
except Exception as e:
    print(f"Error in MQTT loop: {e}")
