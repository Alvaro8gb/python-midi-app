from input.midi import MidiReader, pressed_keys, lock
import time

input_device = MidiReader().getDevice()

while True:
    time.sleep(0.1)
    with lock:
        if len(pressed_keys) > 0:
            print(pressed_keys)