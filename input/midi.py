import mido

class MidiReader():

    def __init__(self, controller):
        self.midi_devices = mido.get_input_names()
        self.controller = controller
        self.running = False

        if len(self.midi_devices) == 0:
            raise Exception("No midi devices found")

        self.input_device = None

    def open(self, midi_device:str):
        self.input_device = mido.open_input(midi_device, callback= self.__run__)

    def close(self):
        if self.input_device is not None:
            self.input_device.close()
            self.input_device = None

            print("Midi close")


    def __run__(self, msg):

        print(msg)
        if msg.type == 'note_on':
            if msg.velocity == 0:
                self.controller.note_off(msg)
            else:
                self.controller.note_on(msg)

        elif msg.type == 'note_off':
            self.controller.note_off(msg)
        else:
            pass


""" MIDI 

velocidad de pulsación" o "velocidad de ataque", 
es un parámetro que se utiliza en el protocolo MIDI para indicar la intensidad con la que se toca una nota musical


En el protocolo MIDI, la velocidad de la nota se representa mediante un valor numérico que varía de 0 a 127. Un valor de velocidad de 0 
se interpreta como una pulsación muy suave o un toque ligero, mientras que un valor de 127 indica una pulsación 
fuerte o un toque muy enérgico.

Es importante tener en cuenta que la interpretación de la velocidad de la nota y cómo afecta al sonido final depende del dispositivo MIDI que 
recibe el mensaje. Algunos dispositivos pueden asignar la velocidad a parámetros específicos, como el volumen o la amplitud del sonido, 
mientras que otros pueden utilizarla para modular otros aspectos 
del sonido, como la expresividad o la respuesta del filtro. Esto puede variar según el sintetizador o el software que se esté utilizando.


"""