import numpy as np
import scipy.signal as signal

from globals import CHUNK
from itertools import zip_longest



class Chunker:

    def group_elements(self, n, iterable, padvalue=0):
        return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)

    def chunkerize(self, sample):
        return [np.float32(chunk) for chunk in self.group_elements(CHUNK, sample)]


class Spliter:

    def split(self, sample):
        # Calcular el tamaño de cada fragmento
        envelope = np.abs(signal.hilbert(sample))

        # Establecemos un umbral para detectar el inicio y el final del sustain
        threshold = 0.1 * np.max(envelope)
        start_index = np.argmax(envelope > threshold)
        end_index = len(envelope) - np.argmax(envelope[::-1] > threshold)

        # Extraemos el sustain del sample
        attack = sample[:start_index]
        sustain = sample[start_index:end_index]
        release = sample[end_index:]


        return attack, sustain, release

