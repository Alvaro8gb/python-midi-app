import sounddevice as sd

from globals import SRATE, CHUNK


class Player:
    def __int__(self):
        self.stream = sd.OutputStream(samplerate=SRATE, blocksize=CHUNK,
                                      channels=1)

    def start(self):
        self.stream.start()

    def close(self):
        self.stream.close()

    def play(self, chunk):
        self.stream.write(chunk)
