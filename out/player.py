import sounddevice as sd

from globals import SRATE, CHUNK


class Player:
    def __init__(self):
        self.stream = sd.OutputStream(samplerate=SRATE, blocksize=CHUNK,
                                      channels=1, latency="high")

    def start(self):
        self.stream.start()

    def close(self):
        self.stream.close()

    def play(self, chunk):
        self.stream.write(chunk)
