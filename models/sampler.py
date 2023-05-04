import os
import numpy as np
from models.NoteFactory import NoteBase, Note
import soundfile as sf
from globals import CHUNK
from models.utils import Spliter

class Sampler(NoteBase):
    __SAMPLES_DIRECTORY = "./samples"
    samples = None
    def __init__(self, note:Note):

        super().__init__()

        if Sampler.samples is None:
            Sampler.samples = Sampler.load_samples()
            print("Samples: ", Sampler.samples.keys())

        do_mas_cercano, distancia_semitonos = Sampler.encontrar_do_mas_cercano(note.note)
        octave = str( (do_mas_cercano // 12) - 1) # C-1 - C11


        self.buffer = None
        if octave in Sampler.samples.keys():
            sample = Sampler.samples[octave]

            if distancia_semitonos > 0:
                ratio = 2 ** (distancia_semitonos / 12)
                sample = np.interp(np.arange(0, len(sample), ratio), np.arange(0, len(sample)), sample).astype(np.float32)

            s = Spliter()

            attack, release = s.split(sample)

            # Calculamos el sustain de la nota
            start_index, end_index = self.detect_sustain(sample)
            sustain = sample[start_index, end_index]

            # Hacemos que el buffer simplemente contenga el sustain calculado previamente
            self.buffer = sustain


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

    def detect_sustain(sample, threshold=0.1):
        # Busca el primer índice donde la amplitud supera el umbral
        start_index = next((i for i, x in enumerate(sample) if abs(x) > threshold), None)

        # Busca el último índice donde la amplitud supera el umbral
        end_index = next((i for i, x in enumerate(reversed(sample)) if abs(x) > threshold), None)

        # Invierte el índice final para obtener su posición en el array original
        if end_index is not None:
            end_index = len(sample) - end_index - 1

        return start_index, end_index

    def next(self):
        if self.buffer is None:
            return np.empty(0, dtype="float32")

        start_index = self.pointer
        end_index = (start_index + CHUNK) % len(self.buffer)

        if start_index < end_index:
            # Caso sencillo: chunk no envuelve el buffer
            chunk = self.buffer[start_index:end_index]
        else:
            # Caso complicado: chunk envuelve el buffer
            chunk = np.concatenate((self.buffer[start_index:], self.buffer[:end_index]))

        self.pointer = (self.pointer + CHUNK) % len(self.buffer)

        return chunk


