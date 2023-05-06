import numpy as np
from math import pow
from globals import SRATE, DECAY
from models.efects import reverb, chorus
from models.NoteFactory import Note, NoteBase


class KarplusStrong:

    def transform(self, note: Note):
        n = SRATE // int(note.frequency)  # la frecuencia determina el tamaño del buffer
        buf = np.random.uniform(-1, 1, n)  # buffer inicial: ruido
        nSamples = int(note.duration * SRATE)
        samples = np.empty(nSamples, dtype="float32")  # salida

        # Parámetros del filtro
        a = 0.5  # Factor de suavizado del filtro
        b = 1 - a  # Factor de conservación del filtro

        pluck_factor = 0.5  # simular cuerda frotada

        # Aplicar el punteo inicial
        buf[int(n * pluck_factor)] = np.random.rand() * 2 - 1

        # Generamos los nSamples haciendo recorrido circular por el buffer
        for i in range(nSamples):
            samples[i] = buf[i % n]  # Recorrido de buffer circular
            buf[i % n] = a * buf[i % n] + b * buf[(1 + i) % n] # Filtrado del buffer


        # Aplicar efectos
        samples = reverb(samples)
        samples, voices = chorus(samples)

        samples = + sum(voices)

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


class Synthesizer(NoteBase):
    velocity_hold = 60

    def __init__(self, note: Note, chunk_size):

        super().__init__(chunk_size)

        self.buff_size = SRATE // int(note.frequency)
        self.buffer = np.random.uniform(-1, 1, self.buff_size) # buffer inicial Ruido
        self.loop = True
        self.pointer = 0
        self.state = "attack"
        self.attack_time = self.calculate_attack_time()

        print(self.attack_time)

        # Parámetros del filtro
        self.a = 0.4  # Factor de suavizado del filtro
        self.b = 1 - self.a  # Factor de conservación del filtro

        # Aplicar atenuacion dependiendo de la velocidad
        attenuation = Synthesizer.get_attenuation(note.velocity)
        self.buffer *= attenuation

    @staticmethod
    def get_attenuation(value):

        limit = Synthesizer.velocity_hold + 20
        if value <= Synthesizer.velocity_hold:
            return value / limit  # Mapear los valores de 0 a velocity_hold linealmente
        elif value > 127:
            return 1.0
        else: # mapeo exponencial
            return Synthesizer.velocity_hold / limit + (
                        0.25 * pow((value - Synthesizer.velocity_hold) / (127 - Synthesizer.velocity_hold), 2))

    def calculate_attack_time(self):
        ATTACK_TIME = 0.3

        attack_samples = int(ATTACK_TIME * SRATE)  # Número de muestras en el tiempo de ataque

        # Calcula el factor de ataque basado en el tamaño del buffer y el tiempo de ataque
        attack_factor = self.buff_size / attack_samples

        # Utiliza el factor de ataque para ajustar el tiempo de ataque según la frecuencia de la nota
        return int(attack_factor * attack_samples)

    def note_off(self):
        self.loop = True
        self.state = "release"

    def next(self):

        chunk = np.empty(self.chunk_size, dtype="float32")

        for i in range(self.chunk_size):
            # Leer el valor actual del buffer
            current_sample = self.buffer[self.pointer]

            if self.attack_time > 0:
                last_sample = self.buffer[(self.pointer - 1) % self.buff_size]

                self.buffer[self.pointer] = DECAY * (self.a * current_sample + self.b * last_sample)

                self.attack_time -= 1

            # elif self.sustain_time > 0:
            #    last_sample = self.buffer[(self.pointer - 1) % self.buff_size]
            #
            #    self.buffer[self.pointer] = DECAY * last_sample
            #
            #    self.sustain_time -= 1
            # else:
            #    self.buffer[self.pointer] = DECAY * self.buffer[self.pointer]

            chunk[i] = current_sample

            self.pointer = (self.pointer + 1) % self.buff_size

        # output = reverb(output)

        return chunk


## Pruebas

def finetune(note):
    # Calculate the length of the buffer
    buffer_length = int(round(note.duration * note.frequency))

    # Generate random noise for the buffer
    buffer = np.random.uniform(-1, 1, buffer_length)

    # Create a delay line with fractional delay
    delay = int(note.frequency)
    delay_fractional = note.frequency - delay
    buffer_length_padded = buffer_length + delay
    delay_line = np.zeros(buffer_length_padded)

    # Create an output signal
    output = np.zeros(buffer_length)

    for i in range(buffer_length):
        # Get the current sample from the delay line
        current_sample = buffer[i]

        # Calculate the index for the fractional delay
        index = int(i + delay)

        # Wrap the index around if it exceeds the size of the delay line
        index %= buffer_length_padded

        # Interpolate between the current and delayed samples
        interpolated_sample = (1 - delay_fractional) * delay_line[index] + delay_fractional * delay_line[
            (index + 1) % buffer_length_padded]

        # Calculate the output sample
        output_sample = DECAY * 0.5 * (current_sample + interpolated_sample)

        # Store the output sample
        output[i] = output_sample

        # Update the delay line
        delay_line = np.roll(delay_line, -1)
        delay_line[-1] = output_sample

    return output
