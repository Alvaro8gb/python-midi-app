import mido

""" 
Se conecta al primer controlador MIDI y escribe mensajes interrumpidamente
"""
import queue
import threading

notes_queue = queue.Queue()
pressed_keys = {}
lock = threading.Lock()


def callback(msg):
    #print(msg)
    with lock:
        if msg.type == 'note_on':
            pressed_keys[msg.note] = msg.velocity
        elif msg.type == 'note_off':
            pressed_keys.pop(msg.note, None)
        else:
            "Otros tipos de mensajes no se hace nada con ellos"
            pass


class MidiReader:

    def __init__(self):
        midi_devices = mido.get_input_names()
        print(midi_devices)

        if len(midi_devices) == 0:
            raise Exception("No midi devices found")

        self.input_device = mido.open_input(midi_devices[0], callback=callback)

    def getDevice(self):
        return self.input_device


def midi2freq(nota_midi):
    """
    Midi consta de 128 notas de [0-127]
    La nota 0 tiene frecuencia 8.17 Hz
    La nota 127 tiene frecuencia 12,54 KHz
    """
    return 2 ** ((nota_midi - 69) / 12) * 440