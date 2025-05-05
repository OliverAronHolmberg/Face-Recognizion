import paho.mqtt.client as mqtt

# MQTT Settings
Broker = "test.mosquitto.org"  # Mqtt adress
Port = 1883
Topic = "oliver/face_detection/alert"

# MQTT client setup
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code: {rc}")

client.on_connect = on_connect

# Anslut till broker
client.connect(Broker, Port, 60)


client.loop_start()

# Medelande funktion
def send_message(message: str):
    """Function to send messages to MQTT broker."""
    try:
        client.publish(Topic, message)
        print(f"Message '{message}' sent to topic '{Topic}'")
    except Exception as e:
        print(f"Error sending message: {e}")
