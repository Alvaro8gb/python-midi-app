import sounddevice as sd

from globals import SRATE, MAX_CHUNK


class Player:
    def __init__(self):
        self.stream = sd.OutputStream(samplerate=SRATE, blocksize=MAX_CHUNK,
                                      channels=1, latency="high")

    def start(self):
        self.stream.start()

    def close(self):
        self.stream.close()

    def play(self, chunk):
        """
        Si el tamaño del chunk es inferior a MAX_CHUNK rellena con ceros
        """
        self.stream.write(chunk)
