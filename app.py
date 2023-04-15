from input import midi

# Este archivo será el que lanzara la app, debera haber 4 hebras:
# 1. Interfaz
# 2. Teclado Midi
# 3. Logica ( Modelos)
# 4. Reproductor de audio

from input.midi import MidiReader, midi2freq
from out.player import Player
from models.note import Note
from models.sintesis import KarplusStrong

if __name__ == '__main__':
    print("Running app")

    sintetizador = KarplusStrong()
    player = Player()
    reader = MidiReader()
    input_device = reader.getDevice()

    player.start()

    for m in input_device:
        print(m)
        note = Note(frequency=midi2freq(m.note), duration=1, note=m.note)
        print(note)

        samples = sintetizador.transform(note)

        player.play(samples)