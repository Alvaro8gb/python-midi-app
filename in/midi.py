import mido

""" 
Se conecta al primer controlador MIDI y escribe mensajes interrumpidamente
"""

midi_devices = mido.get_input_names()
print(midi_devices)

if len(midi_devices) == 0:
    raise Exception("No midi devices found")

input_device = mido.open_input(midi_devices[0])
for msg in input_device:
    print(msg)

    #print(msg.type)
    #print(msg.note)
