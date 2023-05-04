import mido

""" 
Se conecta al primer controlador MIDI y escribe mensajes interrumpidamente
"""
import queue
import threading

from controller import create_note_factor
from models.sintesis import Synthesizer

notes_queue = queue.Queue()
playing_keys = {}
lock = threading.Lock()


def callback(msg):
    print(msg)
    with lock:
        if msg.type == 'note_on':

            if msg.velocity == 0:
                playing_keys[msg.note] = None
            else:
                playing_keys[msg.note] = create_note_factor(msg.note, msg.velocity)

        elif msg.type == 'note_off':
            playing_keys[msg.note] = None
        else:
            "Otros tipos de mensajes no se hace nada con ellos"
            pass

class MidiReader:

    def __init__(self):
        midi_devices = mido.get_input_names()
        print(midi_devices)

        if len(midi_devices) == 0:
            raise Exception("No midi devices found")

        self.input_device = mido.open_input(midi_devices[1], callback=callback)

    def getDevice(self):
        return self.input_device



""" MIDI 

velocidad de pulsación" o "velocidad de ataque", 
es un parámetro que se utiliza en el protocolo MIDI para indicar la intensidad con la que se toca una nota musical


En el protocolo MIDI, la velocidad de la nota se representa mediante un valor numérico que varía de 0 a 127. Un valor de velocidad de 0 
se interpreta como una pulsación muy suave o un toque ligero, mientras que un valor de 127 indica una pulsación 
fuerte o un toque muy enérgico.

Es importante tener en cuenta que la interpretación de la velocidad de la nota y cómo afecta al sonido final depende del dispositivo MIDI que 
recibe el mensaje. Algunos dispositivos pueden asignar la velocidad a parámetros específicos, como el volumen o la amplitud del sonido, 
mientras que otros pueden utilizarla para modular otros aspectos 
del sonido, como la expresividad o la respuesta del filtro. Esto puede variar según el sintetizador o el software que se esté utilizando.


"""