from wit import Wit
from stt import wake_word, stt
from mqtt import mqtt_utils
from os import listdir
from os.path import isfile, join
import importlib
import json
from tts import tts
import playsound
from utils.colors import *

options = {}
with open("./utils/options.json") as f:
    options = json.load(f)

languages = {}
with open("./utils/languages.json") as f:
    languages = json.load(f)

client = Wit(options["wit"])
intents = {}
intent_path = options["intents"]
intent_folders = [f for f in listdir(intent_path) if not isfile(join(intent_path, f))]

for intent_folder in intent_folders:
    if isfile(join(intent_path, intent_folder, "__init__.py")):
        try:
            intents[intent_folder] = importlib.import_module(f"{intent_path}.{intent_folder}.__init__")
            intents[intent_folder] = intents[intent_folder].create_intent()
            intents[intent_folder].initialize()
        except Exception as e:
            print(f"{RED}[INTENT-LOADER] Couldn't load {intent_folder}!")
            print(f"[INTENT-LOADER] {e}{RESET}")
            del intents[intent_folder]
print(f"{BLUE}[INTENT-LOADER] Successfully loaded {len(intents)} intent(s).{RESET}")


def on_wakeword():
    print(f"{MAGENTA}[WAKEWORD-DETECTION] Wakeword detected. Listening...{RESET}")

    mqtt_utils.publish("iap/wakeword", json.dumps({ "wakeword": options["wakeword"] }))
    mqtt_utils.publish("iap/state", json.dumps({ "state": "listening" }))

    playsound.playsound("./rsc/listening.mp3")

    stt_response = stt.recognize()
    print(f"{MAGENTA}[STT] Response: {stt_response}. Analyzing...{RESET}")

    mqtt_utils.publish("iap/state", json.dumps({"state": "thinking"}))

    if stt_response["transcription"]:
        try:
            wit_response = client.message(stt_response["transcription"])
        except:
            print(f"{RED}[WIT AI] Error while calling API!{RESET}")
            if languages.get(options["language"], False):
                tts.say(languages[options["language"]]["error_message"])
            return
        print(f"{YELLOW}[WIT AI] Response: {wit_response}{RESET}")

        if len(wit_response["intents"]) > 0:
            intent_name = wit_response["intents"][0]["name"]

            print(f"{GREEN}[IAP] Intent '{intent_name}' detected. Running 'intent_detected()' in '__init__.py' if available...{RESET}")

            mqtt_utils.notify_intent(wit_response)

            if intents.get(intent_name, False):
                try:
                    intents[intent_name].intent_detected(wit_response)
                    print(f"{GREEN}[IAP] Successfully ran 'intent_detected()' for {intent_name}.{RESET}")
                except Exception as e:
                    print(f"{RED}[IAP] Couldn't run 'intent_detected()' on {intent_name}!")
                    print(f"[{intent_name}] {e}{RESET}")
        else:
            print(f"{RED}[WIT AI] Error while calling API!{RESET}")
            if languages.get(options["language"], False):
                tts.say(languages[options["language"]]["error_message"])
            return

    else:
        # tts.say(options["not_understood"])
        playsound.playsound("./rsc/error.mp3")

    mqtt_utils.publish("iap/state", json.dumps({"state": "finished"}))
    # TODO play sound


wake_word.add_wakeword_callback(on_wakeword)

print(f"{GREEN}[IAP] Started all services successfully.{RESET}")

# Keep main process awake
while True:
    pass

print("[IAP] Stopping...")
