import abc
from pydantic import BaseModel
from typing import Optional


def midi2freq(nota_midi):
    """
    Midi consta de 128 notas de [0-127]
    La nota 0 tiene frecuencia 8.17 Hz
    La nota 127 tiene frecuencia 12,54 KHz
    """
    return 2 ** ((nota_midi - 69) / 12) * 440

def create_note_from_msg(msg):
    return Note(id=msg.note, frequency= midi2freq(msg.note), velocity=msg.velocity)
class Note(BaseModel):
    id: int  # 0-127
    velocity: int # 0-127
    frequency: Optional[float]
    duration: Optional[float]

class NoteBase(abc.ABC):

    def __init__(self, chunk_size):
        self.pointer = 0
        self.chunk_size = chunk_size

    @abc.abstractmethod
    def next(self):
        """
        Return the next chunk
        """
        pass
