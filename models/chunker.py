from itertools import zip_longest
import numpy as np
from globals import CHUNK


class Chunker:
    def group_elements(self, n, iterable, padvalue=0):
        return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)

    def chunkerize(self, sample):
        return [np.float32(chunk) for chunk in self.group_elements(CHUNK, sample)]

