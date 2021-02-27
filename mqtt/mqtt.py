import paho.mqtt.client as mqtt
import json
import threading

options = {}

callbacks = []

with open("./utils/options.json") as f:
    options = json.load(f)


def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected to {options['mqtt_host']}:{options['mqtt_port']}.")
    for sub in options["mqtt_subscriptions"]:
        mqtt_client.subscribe(sub)


def on_message(client, userdata, msg):
    print(f"[MQTT] Message ({msg.topic}): {msg.payload}")
    for callback in callbacks:
        callback(client, userdata, msg)


def add_onmessage_callback(callback):
    callbacks.append(callback)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print(f"[MQTT] Establishing connection to {options['mqtt_host']}:{options['mqtt_port']}...")

mqtt_client.connect(options["mqtt_host"], options["mqtt_port"])

mqtt_thread = threading.Thread(target=mqtt_client.loop_forever, name="MQTT Thread")
mqtt_thread.start()
