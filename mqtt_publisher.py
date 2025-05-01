import paho.mqtt.client as mqtt

# Define the MQTT broker and topic
Broker = "192.168.1.6"  # This should be the IP address of your Raspberry Pi
Port = 1883
Topic = "face_detection/alert"

# The message to be sent
Message = "möthe är bäst"

# Callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code: {rc}")
    # After connection, publish the message to the topic
    client.publish(Topic, Message)
    print(f"Message '{Message}' sent to topic '{Topic}'")
    client.disconnect()  # Disconnect after publishing the message

# Set up MQTT client
client = mqtt.Client()

# Set the callback for when the client connects
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(Broker, Port, 60)

# Start the loop to connect and send the message
client.loop_forever()
