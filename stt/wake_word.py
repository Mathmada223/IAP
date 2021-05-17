import pvporcupine
import pyaudio
import json
import threading
import struct
from utils.colors import *
import utils.logger as logger

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
        logger.log(f"{MAGENTA}[WAKEWORD-DETECTION] Shutting down Wake Word detection....{RESET}")
    finally:
        if handle is not None:
            logger.log(f"{MAGENTA}[WAKEWORD-DETECTION] Shutting down Porcupine Handle...{RESET}")
            handle.delete()
        if audio_stream is not None:
            logger.log(f"{MAGENTA}[WAKEWORD-DETECTION] Shtuting down PyAudio AudioStream...{RESET}")
            audio_stream.close()
        if pa is not None:
            logger.log(f"{MAGENTA}[WAKEWORD-DETECTION] Shutting down PyAudio...")
            pa.terminate()
        logger.log(f"{MAGENTA}[WAKEWORD-DETECTION] Successfully shutted down Wake Word detection{RESET}")


def add_wakeword_callback(callback):
    callbacks.append(callback)


listeningThread = threading.Thread(target=listen, name="Listening Thread")
listeningThread.daemon = True
listeningThread.start()
