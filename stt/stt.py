import speech_recognition as sr
import json

options = {}

with open("./utils/options.json") as f:
    options = json.load(f)


def recognize():
    r = sr.Recognizer()
    m = sr.Microphone()

    with m as source:
        # r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = r.recognize_google(audio, language=options["language"])
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response
