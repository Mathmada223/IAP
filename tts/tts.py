import pyttsx3
import threading


def sync_say(what):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(what)
    engine.runAndWait()


def say(what):
    print(f"[TTS] Saying '{what}'...")
    speak_thread = threading.Thread(target=sync_say, name="TTS Thread", args=(what,))
    speak_thread.start()
