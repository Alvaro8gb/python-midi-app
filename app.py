import concurrent.futures

from input.midi import MidiReader
from out.player import Player

from input.midi import playing_keys, lock

def calculate_chunk(s):
    """
    función para el cálculo de los chunks en paralelo

    """
    return s.next()

if __name__ == '__main__':
    print("Running app")

    player = Player()
    reader = MidiReader()

    notas_actual = []

    input_device = reader.getDevice()

    player.start()

    while True:

        with lock:
            playing_keys_copy = list(playing_keys.values())

        chunks = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Calcular los chunks en paralelo utilizando múltiples hilos
            chunk_futures = [executor.submit(calculate_chunk, s) for s in playing_keys_copy if s is not None]
            # Obtener los resultados de los chunks calculados
            chunks = [future.result() for future in concurrent.futures.as_completed(chunk_futures)]

        if len(chunks) > 0:
            #print("Playing")
            player.play(sum(chunks))