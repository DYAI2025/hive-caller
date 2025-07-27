import time
import pyaudio
import connector.responder as responder


def listen(config):
    """Record audio from microphone for a short duration."""
    duration = config.get('record_seconds', 5)
    rate = config.get('rate', 16000)
    chunk = 1024

    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=rate,
                     input=True, frames_per_buffer=chunk)

    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    pa.terminate()

    # In a real implementation, audio would be passed to a speech-to-text model
    # For now, return dummy text
    return "hello world"


def handle_text(text, config):
    responder.respond(text, config)
