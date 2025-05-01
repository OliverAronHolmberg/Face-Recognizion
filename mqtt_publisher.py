from main import face_detected
import paho.mqtt.client as mqtt

# Variabler inom Mqtt
Broker = "192.168.1.6"  # Raspberry pi adress
Port = 1883
Topic = "face_detection/alert"

# Medelandet
Message = face_detected

# Funktion för när den ansluter till servern
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code: {rc}")
    # Publisera medelandet
    client.publish(Topic, Message)
    print(f"Message '{Message}' sent to topic '{Topic}'")
    client.disconnect()  # Disconnect

# MQTT klienten
client = mqtt.Client()

# Setter callback när den ansluter
client.on_connect = on_connect

# Anslut till MQTT broker
client.connect(Broker, Port, 60)

# Funktionen
client.loop_forever()
