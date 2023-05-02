import numpy as np
from globals import SRATE, CHUNK, DECAY
from models.note import Note
from out.player import Player
from models.utils import Chunker
from models.efects import reverb, chorus


# - Para empezar, tal como os conté en clase, la nota depende del tamaño del buffer de entrada. Este tamaño es un entero, así que para sacar frecuencias no enteras hay que buscar soluciones.
# - El algoritmo que os enseñe aplica un filtro LP elemental al buffer. Investigar otros filtros.
# - El sonido de cuerda que produce KS es "muy seco" (sin caja de resonancia). Podéis colorearlo simulando algún tipo de resonancia, reverb u otro efecto.
# Se puede también añadir algo de desafinación (chorus) para hacerlo más realista.
# - Es posible simular una cuerda frotada variando este algoritmo.


class KarplusStrong:

    def transform(self, note: Note):
        n = SRATE // int(note.frequency)  # la frecuencia determina el tamaño del buffer
        buf = np.random.rand(n) * 2 - 1  # buffer inicial: ruido
        nSamples = int(note.duration * SRATE)
        samples = np.empty(nSamples, dtype="float32")  # salida

        # Parámetros del filtro
        a = 0.5  # Factor de suavizado del filtro
        b = 1 - a  # Factor de conservación del filtro

        pluck_factor = 0.5 # simular cuerda frotada

        # Aplicar el punteo inicial
        buf[int(n * pluck_factor)] = np.random.rand() * 2 - 1

        # Generamos los nSamples haciendo recorrido circular por el buffer
        for i in range(nSamples):
            samples[i] = buf[i % n]  # Recorrido de buffer circular

            # Filtrado del buffer
            buf[i % n] = a * buf[i % n] + b * buf[(1 + i) % n]

        # Aplicar efectos

        samples = reverb(samples)
        samples, voices = chorus(samples)

        samples =+ sum(voices)

        return samples

"""

Implementa el sintetizador de Karplus-Strong utilizando un filtro de retardo de línea con decaimiento exponencial.

En el método set_frequency, la longitud del buffer utilizado para el filtro de retardo de línea se ajusta según la 
frecuencia fundamental de la cuerda que se desea simular. La longitud del buffer es igual a la duración de un ciclo 
completo de la onda de la cuerda simulada, que es igual a la inversa de la frecuencia fundamental.

En el método next, se calcula la salida del sintetizador en bloques de tamaño chunk_size. En cada iteración 
del bucle for, se calcula el valor actual del filtro de retardo de línea, que se almacena en current_sample. 
Luego, se calcula el promedio entre el valor actual y el valor anterior del filtro de retardo de línea, que se 
almacena en average_sample. Este promedio se multiplica por el factor de decaimiento exponencial self.decay para 
simular la pérdida de energía de la cuerda, y se almacena en el buffer del filtro de retardo de línea.

Después de calcular average_sample, el puntero del buffer se incrementa para apuntar al siguiente valor. 
Si el puntero alcanza el final del buffer, se vuelve al inicio.

Finalmente, el valor actual del filtro de retardo de línea (current_sample) se agrega al output, que se
 devuelve al final del método. Cada bloque de output generado por getNextChunk representa un fragmento de la señal de audio de la cuerda simulada.
"""


class Synthesizer:
    def __init__(self, desire_frequency, velocity):

        self.buff_size = SRATE // int(desire_frequency)
        self.buffer = np.random.rand(self.buff_size) * 2 - 1  # buffer inicial Ruido
        self.loop = True
        self.pointer = 0
        self.state = "attack"
        self.attack_time = self.calculate_attack_time(velocity)
        print(self.attack_time)

        # Parámetros del filtro
        self.a = 0.4  # Factor de suavizado del filtro
        self.b = 1 - self.a  # Factor de conservación del filtro

    def calculate_attack_time(self, velocity):
        ATTACK_TIME = 0.1

        attack_samples = int(ATTACK_TIME * SRATE)  # Número de muestras en el tiempo de ataque

        # Calcula el factor de ataque basado en el tamaño del buffer y el tiempo de ataque
        attack_factor = self.buff_size / attack_samples

        # Utiliza el factor de ataque para ajustar el tiempo de ataque según la frecuencia de la nota
        return int(attack_factor * attack_samples) + velocity

    def note_off(self):
        self.loop = True
        self.state = "release"

    def next(self):

        output = np.empty(CHUNK, dtype="float32")

        for i in range(CHUNK):
            # Leer el valor actual del buffer
            current_sample = self.buffer[self.pointer]

            if self.attack_time > 0:
                last_sample = self.buffer[(self.pointer - 1) % self.buff_size]

                self.buffer[self.pointer] = DECAY * (self.a * current_sample + self.b * last_sample)

                self.attack_time -= 1

            #elif self.sustain_time > 0:
            #    last_sample = self.buffer[(self.pointer - 1) % self.buff_size]
#
            #    self.buffer[self.pointer] = DECAY * last_sample
#
            #    self.sustain_time -= 1
            #else:
            #    self.buffer[self.pointer] = DECAY * self.buffer[self.pointer]

            output[i] = current_sample

            self.pointer = (self.pointer + 1) % self.buff_size

        #output = reverb(output)

        return output



## Pruebas

from globals import NOTAS

def static(p):
    chunker = Chunker()
    m = KarplusStrong()

    notes = [m.transform(Note(frequency=NOTAS["C"], duration=3, note=2)),
             m.transform(Note(frequency=NOTAS["B"], duration=1, note=2))
             ]

    for n in notes:
        for c in chunker.chunkerize(n):
            p.play(c)

def continuos(p):
    i = 0

    while True:
        p.play(m.next())
        i += 1

        if i == 10000:
            print("NOte off")
            m.note_off()
            break

    p.play(m.next())


if __name__ == '__main__':
    m = Synthesizer(NOTAS["C"], 100)

    p = Player()
    p.start()

    static(p)
    p.close()
