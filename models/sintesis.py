import numpy as np
from globals import SRATE


def KarplusStrong(frec, dur):
    N = SRATE // int(frec)  # la frecuencia determina el tamanio del buffer
    buf = np.random.rand(N) * 2 - 1  # buffer inicial: ruido
    nSamples = int(dur * SRATE)
    samples = np.empty(nSamples, dtype=float)  # salida
    # generamos los nSamples haciendo recorrido circular por el buffer
    for i in range(nSamples):
        samples[i] = buf[i % N]  # recorrido de buffer circular
        buf[i % N] = 0.5 * (buf[i % N] + buf[(1 + i) % N])  # filtrado

    return samples
