from input.midi import MidiReader
from models.model import Model
from view.board import Interface
from models.NoteFactory import create_note_from_msg


class Controller:
    def __init__(self):
        self.midi_reader = MidiReader(self)
        self.model = Model()
        self.view = Interface(self)

    def start(self):
        self.model.start()
        self.view.run()

    def note_on(self, msg):
        note = create_note_from_msg(msg)
        self.model.play_note(note)
        self.view.press_key(msg.note)

    def note_off(self, msg):
        note = create_note_from_msg(msg)
        self.model.stop_note(note)
        self.view.release_key(msg.note)

    def get_midi_devices(self):
        return self.midi_reader.midi_devices

    def get_model_name(self):
        return self.model.get_model_name()

    def connect_midi_device(self, midi_device):
        self.midi_reader.open(midi_device)

    def disconect_midi_device(self):
        self.midi_reader.close()

    def change_model(self, model_name):
        self.model.change_model(model_name)

    def change_chunk(self, chunk_size):
        self.model.change_chunk(int(chunk_size))

    def end(self):
        self.midi_reader.close()
        self.model.stop()

    def show_error(self, msg):
        self.view.show_pop_up(msg)


if __name__ == '__main__':
    print("Running app")

    controlador = Controller()
    controlador.start()

    print("-"*30, "\n", "Closing app")

