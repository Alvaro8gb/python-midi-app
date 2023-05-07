import matplotlib.pyplot as plt

from globals import NOTAS
from out.player import Player
from models.utils import Chunker
from models.sintesis import KarplusStrong, finetune
from models.NoteFactory import Note

chunker = Chunker()
m = KarplusStrong()

notes = [Note(frequency=NOTAS["C"], duration=3, id=2, velocity=50),
         Note(frequency=NOTAS["B"], duration=1, id=2, velocity=50)]

configurations = {"complex": m.complex,
                  "basic": m.basic,
                  "afinado": m.basic_fractional_delay
                  }


def play(p, func):
    signals = [func(n) for n in notes]

    for s in signals:
        for c in chunker.chunkerize(s):
            p.play(c)

if __name__ == '__main__':
    p = Player()
    p.start()

    print("Afinado")
    play(p, configurations["afinado"])

    print("Karpus Complejo")
    play(p, configurations["complex"])

    print("Basico")
    play(p, configurations["basic"])

    p.close()
