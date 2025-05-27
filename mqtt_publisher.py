import paho.mqtt.client as mqtt

# MQTT Settings
Broker = "test.mosquitto.org"  # Mqtt adress // Lägg till .org på Pi också
Port = 1883 # Standard Mqtt-port
Topic = "oliver/face_detection/alert" # Mqtt topic

# MQTT client setup
client = mqtt.Client()

# Funktionen som körs när anslutningen till Mqtt-servern är klart
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code: {rc}")


client.on_connect = on_connect

# Anslut till broker
client.connect(Broker, Port, 60)

# Starta Mqtt-klientens loop för att hantera meddelanden
client.loop_start()

# Funktionen som skickar meddelanden till mqtt-server
def send_message(message: str):
    """Function to send messages to MQTT broker."""
    try:
        client.publish(Topic, message)
        print(f"Message '{message}' sent to topic '{Topic}'")
    except Exception as e:
        print(f"Error sending message: {e}")
