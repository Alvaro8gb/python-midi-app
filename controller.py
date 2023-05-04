from models.sintesis import Synthesizer
from models.sampler import Sampler
from models.NoteFactory import Note

player = 0


def create_note_factor(note, velocity):
    note = Note(note=note, frequency=midi2freq(note), velocity=velocity)

    if player == 0:
        return Synthesizer(note)
    else:
        return Sampler(note)


def midi2freq(nota_midi):
    """
    Midi consta de 128 notas de [0-127]
    La nota 0 tiene frecuencia 8.17 Hz
    La nota 127 tiene frecuencia 12,54 KHz
    """
    return 2 ** ((nota_midi - 69) / 12) * 440
