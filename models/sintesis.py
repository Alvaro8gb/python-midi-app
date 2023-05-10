import numpy as np
from math import pow
from globals import SRATE, DECAY
from models.efects import reverb, chorus
from models.NoteFactory import Note, NoteBase


class KarplusStrong:
    """
    Karplus-strong sabiendo la duracion de la nota

    basic: filtro 0.5
    complex: como si fuera una cuerda frotada + eco + chorus + filtro a, b
    basic_fractional_delay: finetune Karplus Strong

    """

    def basic(self, note: Note):
        buff_size = SRATE // int(note.frequency)  # la frecuencia determina el tamanio del buffer
        buf = np.random.uniform(-1, 1, buff_size)  # buffer inicial: ruido
        nSamples = int(note.duration * SRATE)
        samples = np.empty(nSamples, dtype=float)  # salida

        # generamos los nSamples haciendo recorrido circular por el buffer
        for i in range(nSamples):
            actual = buf[i % buff_size]
            siguiente = buf[(i + 1) % buff_size]

            samples[i] = actual
            buf[i % buff_size] = 0.5 * (actual + siguiente)  # # Filtrado del buffer

        return samples

    def complex(self, note: Note):
        buff_size = round(SRATE // note.frequency)  # la frecuencia determina el tamaño del buffer
        buf = np.random.uniform(-1, 1, buff_size)  # buffer inicial: ruido
        nSamples = int(note.duration * SRATE)
        samples = np.empty(nSamples, dtype="float32")  # salida

        # Parámetros del filtro
        a = 0.4  # Factor de suavizado del filtro
        b = 1 - a  # Factor de conservación del filtro

        pluck_factor = 0.5  # simular cuerda frotada

        # Aplicar el punteo inicial
        buf[int(buff_size * pluck_factor)] = np.random.rand() * 2 - 1

        # Generamos los nSamples haciendo recorrido circular por el buffer
        for i in range(nSamples):
            actual = buf[i % buff_size]
            siguiente = buf[(i + 1) % buff_size]

            samples[i] = actual
            buf[i % buff_size] = a * actual + b * siguiente  # Filtrado del buffer

        # Aplicar efectos
        samples = reverb(samples)
        samples, voices = chorus(samples)

        samples = + sum(voices)

        return samples

    def basic_fractional_delay(self, note: Note, delay=0.05):
        interp_factor = 2  # factor de interpolación
        efs = SRATE / interp_factor / note.frequency  # frecuencia efectiva de muestreo
        buff_size = int(efs)  # tamaño del buffer
        buf = np.random.uniform(-1, 1, buff_size)  # buffer inicial: ruido
        nSamples = int(note.duration * SRATE)
        samples = np.empty(nSamples, dtype="float32")  # salida
        pos = 0  # posición actual en el buffer
        for i in range(nSamples):
            n = pos
            tau = pos - n
            n1 = (n + 1) % buff_size
            y = (1 - tau) * buf[n] + tau * buf[n1]  # interpolación
            samples[i] = y
            buf[n] = 0.5 * (y + buf[n1])  # filtrado
            pos = int((pos + interp_factor - delay) % buff_size) # avance en el buffer con interpolación y retardo

        return samples


class Synthesizer(NoteBase):
    velocity_hold = 60
    attack_time = 0.3  # segundos

    def __init__(self, note: Note, chunk_size):

        super().__init__(chunk_size)

        self.attenuation = Synthesizer.get_attenuation(note.velocity)

        self.pointer = 0

        # Parámetros del filtro
        self.a = 0.4  # Factor de suavizado del filtro
        self.b = 1 - self.a  # Factor de conservación del filtro

    @staticmethod
    def get_attenuation(value):

        limit = Synthesizer.velocity_hold + 20
        if value <= Synthesizer.velocity_hold:
            return value / limit  # Mapear los valores de 0 a velocity_hold linealmente
        elif value > 127:
            return 1.0
        else:  # mapeo exponencial
            return Synthesizer.velocity_hold / limit + (
                    0.25 * pow((value - Synthesizer.velocity_hold) / (127 - Synthesizer.velocity_hold), 2))

    @staticmethod
    def calculate_attack_time(buff_size):

        attack_samples = int(Synthesizer.attack_time * SRATE)  # Número de muestras en el tiempo de ataque

        # Calcula el factor de ataque basado en el tamaño del buffer y el tiempo de ataque
        attack_factor = buff_size / attack_samples

        # Utiliza el factor de ataque para ajustar el tiempo de ataque según la frecuencia de la nota
        return int(attack_factor * attack_samples)

class SynthesizerBasic(Synthesizer):
    velocity_hold = 60

    def __init__(self, note: Note, chunk_size):

        super().__init__(note, chunk_size)

        self.buff_size = SRATE // int(note.frequency)
        self.buffer = np.random.uniform(-1, 1, self.buff_size)  # buffer inicial Ruido

        self.state = "attack"
        self.attack_time = Synthesizer.calculate_attack_time(self.buff_size)


        # Aplicar atenuacion dependiendo de la velocidad
        self.buffer *= self.attenuation


    def note_off(self):
        self.state = "release"

    def next(self):

        chunk = np.empty(self.chunk_size, dtype="float32")

        for i in range(self.chunk_size):

            current_sample = self.buffer[self.pointer]

            if self.attack_time > 0:  # Aplicar filtro solo si esta en fase de ataque
                last_sample = self.buffer[(self.pointer - 1) % self.buff_size]

                self.buffer[self.pointer] = DECAY * (self.a * current_sample + self.b * last_sample)

                self.attack_time -= 1

            chunk[i] = current_sample

            self.pointer = (self.pointer + 1) % self.buff_size


        return chunk


class SynthesizerTuned(Synthesizer):
    velocity_hold = 60
    delay = 0.05
    interp_factor = 2  # factor de interpolación

    def __init__(self, note: Note, chunk_size):

        super().__init__(note, chunk_size)

        efs = SRATE / SynthesizerTuned.interp_factor / note.frequency  # frecuencia efectiva de muestreo
        self.buff_size = int(efs)
        self.buffer = np.random.uniform(-1, 1, self.buff_size)  # buffer inicial Ruido

        self.state = "attack"

        self.attack_time = 200

        # Aplicar atenuacion dependiendo de la velocidad
        self.buffer *= self.attenuation

    def note_off(self):
        self.state = "release"

    def next(self):

        chunk = np.empty(self.chunk_size, dtype="float32")

        for i in range(self.chunk_size):

            n = self.pointer
            tau = self.pointer - n
            siguiente = self.buffer[(n + 1) % self.buff_size]
            y = (1 - tau) * self.buffer[n] + tau * siguiente  # interpolación

            chunk[i] = y

            if self.attack_time > 0:  # Aplicar filtro solo si esta en fase de ataque
                self.buffer[n] = 0.5 * (y + siguiente)  # filtrado
                self.attack_time -= 1
                self.pointer = int((self.pointer + SynthesizerTuned.interp_factor - SynthesizerTuned.delay) % self.buff_size)
            else:
                self.pointer = (self.pointer + 1) % self.buff_size

        #chunk = reverb(chunk) peta :(

        return chunk


"""  

Pruebas
"""


def finetune(note: Note):
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
