import numpy as np

from globals import SRATE
from models.note import Note


# - Para empezar, tal como os conté en clase, la nota depende del tamaño del buffer de entrada. Este tamaño es un entero, así que para sacar frecuencias no enteras hay que buscar soluciones.
# - El algoritmo que os enseñe aplica un filtro LP elemental al buffer. Investigar otros filtros.
# - El sonido de cuerda que produce KS es "muy seco" (sin caja de resonancia). Podéis colorearlo simulando algún tipo de resonancia, reverb u otro efecto. Se puede también añadir algo de desafinación (chorus) para hacerlo más realista.
# - Es posible simular una cuerda frotada variando este algoritmo.


class KarplusStrong:

    def transform(self, note: Note):
        n = SRATE // int(note.frequency)  # la frecuencia determina el tamanio del buffer
        buf = np.random.rand(n) * 2 - 1  # buffer inicial: ruido
        nSamples = int(note.duration * SRATE)
        samples = np.empty(nSamples, dtype=float)  # salida
        # generamos los nSamples haciendo recorrido circular por el buffer
        for i in range(nSamples):
            samples[i] = buf[i % n]  # recorrido de buffer circular
            buf[i % n] = 0.5 * (buf[i % n] + buf[(1 + i) % n])  # filtrado

        return samples.astype(np.float32)
