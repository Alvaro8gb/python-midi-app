import abc
from pydantic import BaseModel
from typing import Optional

class Note(BaseModel):
    note: int  # 0-127
    velocity: int # 0-127
    frequency: Optional[float]
    duration: Optional[float]

class NoteBase(abc.ABC):

    def __init__(self):
        self.pointer = 0

    @abc.abstractmethod
    def next(self):
        """
        Return the next chunk
        """
        pass
