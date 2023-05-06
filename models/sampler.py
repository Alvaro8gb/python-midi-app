import os
import numpy as np
from models.NoteFactory import NoteBase, Note
import soundfile as sf
from globals import CHUNK
from models.utils import Spliter

s = Spliter()

class Sampler(NoteBase):
    __SAMPLES_DIRECTORY = "./samples"
    samples = None
    def __init__(self, note:Note, chunk_size):

        super().__init__(chunk_size)

        if Sampler.samples is None:
            Sampler.samples = Sampler.load_samples()
            print("Samples: ", Sampler.samples.keys())

        do_mas_cercano, distancia_semitonos = Sampler.encontrar_do_mas_cercano(note.id)
        octave = str( (do_mas_cercano // 12) - 1) # C-1 - C11


        self.buffer = None
        if octave in Sampler.samples.keys():
            sample = Sampler.samples[octave]

            if distancia_semitonos > 0:
                ratio = 2 ** (distancia_semitonos / 12)
                sample = np.interp(np.arange(0, len(sample), ratio), np.arange(0, len(sample)), sample).astype(np.float32)

            # Calculamos el sustain de la nota
            sustain = Sampler.get_sustain(sample)
            self.buffer = sustain
            self.buff_size = len(sustain)

    @staticmethod
    def encontrar_do_mas_cercano(nota_midi):
        # Calcular la distancia a la nota MIDI de "Do" más cercana
        distancia = round(nota_midi) % 12

        # Calcular el valor MIDI de la nota "Do" más cercana
        do_mas_cercano = round(nota_midi) - distancia

        # Calcular la distancia en semitonos
        distancia_semitonos = abs(nota_midi - do_mas_cercano)

        return do_mas_cercano, distancia_semitonos

    @staticmethod
    def load_samples():
        samples = {}

        for file in os.listdir(Sampler.__SAMPLES_DIRECTORY):
            if file.startswith('C') and file.endswith('.wav'):
                octave = file[1:-4]  # Extraer el número del nombre del file
                path = os.path.join(Sampler.__SAMPLES_DIRECTORY, file)

                if octave.isdigit():
                    sample, srate = sf.read(path, dtype="float32")
                    samples[octave] = sample

        return samples

    @staticmethod
    def get_sustain(sample):

        _ , sustain, _ = s.split(sample)

        return sustain

    def next(self):
        if self.buffer is None:
            return np.empty(0, dtype="float32")

        chunk = np.roll(self.buffer, -self.pointer)[:CHUNK].astype('float32')
        self.pointer = (self.pointer + CHUNK) % self.buff_size

        return chunk
