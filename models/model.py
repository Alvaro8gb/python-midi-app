
import threading
from models.NoteFactory import Note
from models.sampler import Sampler
from models.sintesis import SynthesizerBasic, SynthesizerTuned
from out.player import Player
from globals import MAX_CHUNK

id_to_model = {"sintetizador tunned": 0, "sintetizador basic": 1,  "sampler": 2}
model_to_id = {0: "sintetizador tunned", 1: "sintetizador basic", 2: "sampler"}

class Model:

    def __init__(self):

        self.thread = threading.Thread(target=self.run)

        self.stop_flag = threading.Event()
        self.lock_playing_keys = threading.Lock()
        self.lock_parameters = threading.Lock()

        self.playing_notes = {}

        self.player = Player()

        self.model = 0

        self.chunk_size = MAX_CHUNK


    def get_model_name(self):
        return model_to_id[self.model]

    def change_model(self, id:str):
        with self.lock_parameters:
            if id in id_to_model:
                self.model = id_to_model[id]

    def change_chunk(self, chunk_size:int):
        with self.lock_parameters:
            self.chunk_size = chunk_size

    def run(self):

        while not self.stop_flag.is_set():

            with self.lock_playing_keys:
                playing_notes_copy = list(self.playing_notes.values())

            chunks = [ note.next() for note in playing_notes_copy if note is not None]

            if len(chunks) > 0:
                #print("Playing")
                self.player.play(sum(chunks))


    def start(self):
        self.player.start()
        self.thread.start()

    def stop(self):
        self.stop_flag.set()

    def get_note(self, note:Note):

        with self.lock_parameters:
            if self.model == 0:
                return SynthesizerTuned(note, self.chunk_size)
            elif self.model == 1:
                return SynthesizerBasic(note, self.chunk_size)
            else:
                return Sampler(note, self.chunk_size)

    def play_note(self, note:Note):
        with self.lock_playing_keys:
            self.playing_notes[note.id] = self.get_note(note)

    def stop_note(self, note:Note):
        with self.lock_playing_keys:
            self.playing_notes[note.id] = None

