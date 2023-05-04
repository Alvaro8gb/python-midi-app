from globals import SRATE
from models.utils import Spliter
import numpy as np

def reverb(signal, delay=1, decay=0.5):
    """

    delay Retardo en segundos
    decay Factor de decaimiento

    """

    # Crear la señal de reverberación inicial
    reverb_signal = np.zeros_like(signal)

    # Crear la señal de eco
    echo = np.zeros(int(delay * SRATE))

    # Aplicar el efecto de reverberación
    for i in range(len(signal)):
        # Actualizar el valor del eco
        echo_value = signal[i] + decay * echo[0]

        # Desplazar el eco hacia la derecha
        echo = np.roll(echo, -1)

        # Agregar el valor actual al final del eco
        echo[-1] = echo_value

        # Agregar la señal original y el eco a la señal de reverberación
        reverb_signal[i] = signal[i] + echo_value

    return reverb_signal


def chorus(signal, delay=0.03, depth=0.003, rate=1.5, feedback=0.3):
    # Tamaño del delay en muestras
    delay_samples = int(delay * SRATE)
    # Amplitud de la modulación en muestras
    modulation_amplitude = int(depth * SRATE)

    # Frecuencia de la modulación en Hz
    modulation_frequency = rate

    # Factor de retroalimentación para realimentar la señal
    feedback_factor = feedback

    # Crear señales vacías para las voces del coro
    num_voices = 3
    voices = np.zeros((num_voices, len(signal)))

    # Aplicar el efecto de chorus
    for i in range(num_voices):
        # Calcular el desfase y la amplitud de modulación para la voz actual
        phase_offset = i * 2 * np.pi / num_voices
        modulation = modulation_amplitude * np.sin(2 * np.pi * modulation_frequency * np.arange(len(signal)) / 44100 + phase_offset)

        # Calcular la posición de la muestra retrasada y modulada
        delayed_modulated_position = np.arange(len(signal)) - delay_samples + modulation

        # Calcular los índices enteros de las muestras retrasadas y moduladas
        delayed_modulated_index = np.floor(delayed_modulated_position).astype(int)

        # Calcular las fracciones para la interpolación lineal
        fraction = delayed_modulated_position - delayed_modulated_index

        # Realizar la interpolación lineal para obtener las muestras retrasadas y moduladas
        delayed_modulated_samples = (1 - fraction) * signal[delayed_modulated_index] + fraction * signal[delayed_modulated_index + 1]

        # Realimentar la señal para agregar más cuerpo al coro
        signal += feedback_factor * delayed_modulated_samples

        # Guardar la voz actual en el arreglo de voces
        voices[i] = delayed_modulated_samples

    # Normalizar la señal resultante
    signal /= np.max(np.abs(signal))

    return signal, voices

def envelope(signal):
    s = Spliter()
    length = len(signal)
    attack_samples, sustain_samples, release_samples = s.split(signal)

    # Calcular los índices de los segmentos de ataque, sostenimiento y liberación
    attack_end = min(attack_samples, length)
    sustain_end = min(attack_samples + sustain_samples, length)
    release_start = max(length - release_samples, 0)

    # Calcular las ganancias para cada segmento
    attack_gain = np.linspace(0, 1, attack_end)
    sustain_gain = np.ones(sustain_end - attack_end)
    release_gain = np.linspace(1, 0, length - release_start)

    # Aplicar las ganancias al chunk
    signal[:attack_end] *= attack_gain
    signal[attack_end:sustain_end] *= sustain_gain
    signal[release_start:] *= release_gain

    return signal