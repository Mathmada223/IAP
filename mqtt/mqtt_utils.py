from mqtt import mqtt
import json
from tts import tts

options = {}

with open("./utils/options.json") as f:
    options = json.load(f)


def on_message(client, userdata, msg):
    print("[MQTT-Utils] Processing message...")
    if msg.topic == "iap/tts/say":
        tts.say(msg.payload.decode("UTF-8"))


mqtt.add_onmessage_callback(on_message)


def notify_intent(wit_response):
    intent_name = wit_response["intents"][0]["name"]
    mqtt.mqtt_client.publish(f"{options['base_topic']}/{intent_name}", json.dumps(wit_response))


def publish(topic, payload):
    mqtt.mqtt_client.publish(topic, payload)