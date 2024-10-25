import paho.mqtt.client as mqtt
import boto3
import re

# MQTT configuration
mqtt_broker = "54.252.174.24"  # IP for the MQTT broker
mqtt_port = 1883  # Standard MQTT port
mqtt_topic = "temperature_data"

# Temperature threshold
temperature_threshold = 21  # Set temperature threshold

# AWS SNS configuration
sns_client = boto3.client(
    'sns',
    region_name='ap-southeast-2',  # Your AWS region
    aws_access_key_id='',  # Your actual Access Key ID
    aws_secret_access_key=''  # Your actual Secret Access Key
)

# Function to send SNS alert
def send_sns_alert(subject, message):
    try:
        response = sns_client.publish(
            TopicArn='arn:aws:sns:ap-southeast-2:656123187861:tempcheck',  # Replaced with your SNS Topic ARN
            Message=message,
            Subject=subject
        )
        print("SNS alert sent:", response)
except Exception as e:
        print(f"Failed to send SNS alert: {e}")

def on_message(client, userdata, message):
    data = message.payload.decode()
    print(f"Received data: {data}")

    # Use regex to extract the temperature value
    temperature_match = re.search(r"Temperature:\s+(\d+\.\d+)C", data)

    if temperature_match:
        temperature_str = temperature_match.group(1)
        try:
            temperature = float(temperature_str)
            print(f"Extracted temperature: {temperature}°C")

            # Check if the temperature exceeds the threshold
            if temperature > temperature_threshold:
                alert_message = f"Temperature alert: {temperature}°C is above the threshold of {temperature_threshold}°C."
                send_sns_alert("Temperature Alert", alert_message)
        except ValueError:
            print("Failed to convert extracted temperature to float.")
    else:
        print("Temperature value not found in the message.")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker successfully")
client.subscribe(mqtt_topic)
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")

# Configure the MQTT client
mqtt_client = mqtt.Client()

try:
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect  # Correct callback name
    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.loop_start()

    # Keep the script running
    while True:
        pass

except Exception as e:
    print(f"Error: {e}")
