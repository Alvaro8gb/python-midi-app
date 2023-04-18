from input.midi import MidiReader, midi2freq
from out.player import Player
from models.note import Note
from models.sintesis import KarplusStrong
from models.chunker import Chunker

import threading
from input.midi import notes_queue, pressed_keys, lock
import time

playing_keys = {}
def read_msgs():

    while True:

        time.sleep(0.2)
        with lock:

            if len(pressed_keys) > 0:

                #for note, velocity in pressed_keys.items():
                #    if note not in pressed_old:
                #        sample = sintetizador.transform(note)
                #        chunks = chunker.chunkerize(sample)
                #
                #
                #for note in pressed_old:
                #
                #pressed_old = pressed_keys.values()


                for note, velocity in pressed_keys.items():
                    notes_queue.put(Note(frequency=midi2freq(note), duration=1, note=note))



if __name__ == '__main__':
    print("Running app")

    sintetizador = KarplusStrong()
    player = Player()
    reader = MidiReader()
    chunker = Chunker()

    notas_actual = []

    input_device = reader.getDevice()

    player.start()

    tecla_thread = threading.Thread(target=read_msgs, args=(input_device,))
    tecla_thread.start()

    while True:
        # Comprobamos si hay algún mensaje MIDI en la cola
        if not notes_queue.empty():
            note = notes_queue.get()

            print(note)

            sample = sintetizador.transform(note)
            chunks = chunker.chunkerize(sample)
            notas_actual.append(chunks)

        # Reproducir notas
        if len(notas_actual) > 0:
            samples = [chunks.pop(0) for chunks in notas_actual]

            notas_actual = [chunks for chunks in notas_actual if
                            len(chunks) > 0]

            player.play(sum(samples))
