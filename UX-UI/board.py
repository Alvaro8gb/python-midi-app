import math
import tkinter as tk
import tkinter.messagebox as messagebox
import mido
import threading

# Define las dimensiones de la ventana y el tamaño de cada tecla  
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
KEY_WIDTH = WINDOW_WIDTH // 14
KEY_HEIGHT = int(WINDOW_HEIGHT * 0.75)

# Define la lista de colores de las teclas  
midi_to_chord2 = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B'
}
class Piano:
    def __init__(self, master):
        # Crea el lienzo en el que se dibujarán las teclas
        self.KEY_COLORS = ["white", "black", "white", "black", "white", "white", "black",
                      "white", "black", "white", "black", "white"]
        self.canvas = tk.Canvas(master, width=WINDOW_WIDTH,
                                height=WINDOW_HEIGHT)
        self.canvas.pack()
        self.key_status = {}
        self.labels=[]
        # Crea los botones para cada tecla y los almacena en una lista  
        self.buttons = []
        for i in range(len(self.KEY_COLORS)):
            x = i * KEY_WIDTH
            y = 0
            color = self.KEY_COLORS[i]
            button = tk.Button(self.canvas, bg=color, activebackground=color,
                               borderwidth=1, highlightthickness=3, highlightbackground="black")
            button.place(x=x, y=y, width=KEY_WIDTH, height=KEY_HEIGHT)
            label = tk.Label(self.canvas, text="", bg="white")
            label.place(x=x, y=y + KEY_HEIGHT)
            self.buttons.append(button)
            self.labels.append(label)
            self.key_status[i] = False
        connect_button = tk.Button(master, text="Conectar MIDI", command=self.connect)
        connect_button.place(x=540, y=0)

    def run(self):
        # Inicia el bucle de eventos de la ventana  
        tk.mainloop()
    # Crea una ventana y un objeto Piano
    def connect(self):
        midi_devices = mido.get_input_names()
        print(midi_devices)

        if len(midi_devices) == 0:
            messagebox.showerror("Error", "No se encontraron dispositivos MIDI")

        else:
            messagebox.showinfo("success", "Teclado "+midi_devices[0]+" conectado correctamente")
            input_device = mido.open_input(midi_devices[0])

            def read_input_device():

                for message in input_device:
                    if message.type == 'note_on' and message.velocity > 0:
                    # Llama a la función on_key_pressed con la nota correspondiente
                        self.pulsado(message)
                    elif message.type == 'note_on' and message.velocity == 0:
                        self.soltado(message)
                    # Aquí puedes definir cualquier acción que deba ocurrir cuando se libera una tecla
                    threading.Thread(target=read_input_device).start()

    def on_key_pressed(self, key):
        # Aquí puedes definir la acción que se debe realizar cuando se presiona la tecla 'key'
        print(f"Tecla {key} pulsada")
    def pulsado(self, message):
        # Cambia el color del botón cuando se presiona
        print(message)
        if(self.key_status[message.note % 12] == False):
            self.key_status[message.note % 12] = True
            button = self.buttons[message.note % 12]
            self.KEY_COLORS[message.note % 12] = button.cget('bg')
            button.config(bg="red", activebackground="red")
            mensaje=self.midi_to_chord(message.note)
            self.labels[message.note % 12].config(text=mensaje)

    def soltado(self, message):
        # Restaura el color original del botón
        print(message)
        if(self.key_status[message.note % 12] == True):
            self.key_status[message.note % 12] = False
            button = self.buttons[message.note % 12]
            button.config(bg=self.KEY_COLORS[message.note % 12], activebackground=self.KEY_COLORS[message.note % 12])
            self.labels[message.note % 12].config(text="")

    def midi_to_chord(self,midi_note):
        # Obtener el número de tono y el número de octava
        tone = midi_note % 12
        octave = midi_note // 12 - 1

        # Obtener el símbolo de acorde correspondiente
        chord_symbol = midi_to_chord2[tone]

        # Agregar el número de octava al símbolo de acorde
        chord_notation = f'{chord_symbol}{octave}'

        return chord_notation


root = tk.Tk()
root.title("Piano Digital")
root.geometry("650x300")
root.resizable(False, False)
root.configure(borderwidth=1, highlightthickness=1, highlightbackground="black")
piano = Piano(root)

# Inicia el bucle de eventos de la ventana  
piano.run()
