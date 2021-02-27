import pvporcupine
import pyaudio
import json
import threading
import struct

options = {}

callbacks = []

with open("./utils/options.json") as f:
    options = json.load(f)


def listen():
    try:
        handle = pvporcupine.create(keywords=[options["wakeword"]])
        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=handle.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=handle.frame_length
        )

        while True:
            pcm = audio_stream.read(handle.frame_length)
            pcm = struct.unpack_from("h" * handle.frame_length, pcm)
            keyword_index = handle.process(pcm)

            if keyword_index >= 0:
                for callback in callbacks:
                    callback()
    except KeyboardInterrupt:
        print("[WAKEWORD-DETECTION] Shutting down Wake Word detection....")
    finally:
        if handle is not None:
            print("[WAKEWORD-DETECTION] Shutting down Porcupine Handle...")
            handle.delete()
        if audio_stream is not None:
            print("[WAKEWORD-DETECTION] Shtuting down PyAudio AudioStream...")
            audio_stream.close()
        if pa is not None:
            print("[WAKEWORD-DETECTION] Shutting down PyAudio...")
            pa.terminate()
        print("[WAKEWORD-DETECTION] Successfully shutted down Wake Word detection")


def add_wakeword_callback(callback):
    callbacks.append(callback)


listeningThread = threading.Thread(target=listen, name="Listening Thread")
listeningThread.daemon = True
listeningThread.start()
