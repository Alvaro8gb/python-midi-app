from itertools import zip_longest
import numpy as np
from globals import CHUNK, ATACK_R, SUSTAIN_R, RELEASE_R


class Chunker:

    def group_elements(self, n, iterable, padvalue=0):
        return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)

    def chunkerize(self, sample):
        return [np.float32(chunk) for chunk in self.group_elements(CHUNK, sample)]


class Spliter:

    def split(self, samples):
        # Calcular el tamaño de cada fragmento
        n_attact = int(len(samples) * ATACK_R)  # 10%
        n_sustain = int(len(samples) * SUSTAIN_R)  # 80%
        n_release = int(len(samples) * RELEASE_R)

        # Dividir el array en tres fragmentos
        attack = samples[:n_attact]
        sustain = samples[n_attact:n_attact + n_sustain]
        release = samples[-n_release:]

        return attack, sustain, release

