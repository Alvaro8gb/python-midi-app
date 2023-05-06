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
        self.labels = []
        self.input_device = None
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
            label.place(x=x+17, y=y + KEY_HEIGHT)
            self.buttons.append(button)
            self.labels.append(label)
            self.key_status[i] = False
        connect_button = tk.Button(master, text="Conectar MIDI", command=self.mostrar_desplegable)
        connect_button.place(x=540, y=0)
        mode_button = tk.Button(master, text="Modo", command=self.mostrar_desplegable_modo)
        mode_button.place(x=540, y=100)
        tk.Label(self.canvas, text="chunk:", bg="white").place(x=520, y=40)

        self.spinbox = tk.Spinbox(root,values=(64,256,512),width=15,command=self.on_spinbox_change)
        self.spinbox.place(x=540, y=70)

    def run(self):
        # Inicia el bucle de eventos de la ventana  
        tk.mainloop()

    def mostrar_desplegable(self):
        midi_devices = mido.get_input_names()
        if len(midi_devices) == 0:
            messagebox.showerror("Error", "No se encontraron dispositivos MIDI")
        else:
            self.ventana = tk.Toplevel()
            etiqueta = tk.Label(self.ventana, text="Selecciona una opción:")
            etiqueta.pack()
            self.seleccion = tk.StringVar()
            self.seleccion.set(midi_devices[0])
            desplegable = tk.OptionMenu(self.ventana, self.seleccion, *midi_devices)
            desplegable.pack()
            boton_confirmar = tk.Button(self.ventana, text="Confirmar", command=self.confirmar)
            boton_confirmar.pack()
            ancho_ventana = 200
            altura_ventana = 100
            x = root.winfo_x() + (root.winfo_width() - ancho_ventana) // 2
            y = root.winfo_y() + (root.winfo_height() - altura_ventana) // 2
            self.ventana.geometry(f"{ancho_ventana}x{altura_ventana}+{x}+{y}")
    def confirmar(self):
        if(self.input_device!=None):
            self.input_device.close()
        self.input_device = mido.open_input(self.seleccion.get())
        my_thread = threading.Thread(target=piano.read_input_device)
        my_thread.start()
        self.ventana.destroy()

    def mostrar_desplegable_modo(self):
        self.opciones_modo=["sintetizador","sampler"]
        self.ventana = tk.Toplevel()
        etiqueta = tk.Label(self.ventana, text="Selecciona un modo:")
        etiqueta.pack()
        self.seleccion_modo = tk.StringVar()
        self.seleccion_modo.set(self.opciones_modo[0])
        desplegable = tk.OptionMenu(self.ventana, self.seleccion_modo, *self.opciones_modo)
        desplegable.pack()
        boton_confirmar_modo = tk.Button(self.ventana, text="Confirmar", command=self.confirmar_modo)
        boton_confirmar_modo.pack()
        ancho_ventana = 200
        altura_ventana = 100
        x = root.winfo_x() + (root.winfo_width() - ancho_ventana) // 2
        y = root.winfo_y() + (root.winfo_height() - altura_ventana) // 2
        self.ventana.geometry(f"{ancho_ventana}x{altura_ventana}+{x}+{y}")

    def confirmar_modo(self):
        if (self.seleccion_modo.get()==self.opciones_modo[0]):
            print("xd")
        else:
            print("xd2")
        self.ventana.destroy()

    def read_input_device(self):

        for message in self.input_device:
            if message.type == 'note_on' and message.velocity > 0:
                self.pulsado(message)
            elif message.type == 'note_on' and message.velocity == 0:
                self.soltado(message)


    def pulsado(self, message):
        # Cambia el color del botón cuando se presiona
        print(message)
        if (self.key_status[message.note % 12] == False):
            self.key_status[message.note % 12] = True
            button = self.buttons[message.note % 12]
            self.KEY_COLORS[message.note % 12] = button.cget('bg')
            button.config(bg="red", activebackground="red")
            mensaje = self.midi_to_chord(message.note)
            self.labels[message.note % 12].config(text=mensaje)

    def soltado(self, message):
        # Restaura el color original del botón
        print(message)
        if (self.key_status[message.note % 12] == True):
            self.key_status[message.note % 12] = False
            button = self.buttons[message.note % 12]
            button.config(bg=self.KEY_COLORS[message.note % 12], activebackground=self.KEY_COLORS[message.note % 12])
            self.labels[message.note % 12].config(text="")

    def midi_to_chord(self, midi_note):
        # Obtener el número de tono y el número de octava
        tone = midi_note % 12
        octave = midi_note // 12 - 1
        # Obtener el símbolo de acorde correspondiente
        chord_symbol = midi_to_chord2[tone]
        # Agregar el número de octava al símbolo de acorde
        chord_notation = f'{chord_symbol}{octave}'

        return chord_notation

    def on_spinbox_change(self):

        print("Spinbox value changed:", self.spinbox.get())

root = tk.Tk()
root.title("Piano Digital")
root.geometry("650x300")
root.resizable(False, False)
root.configure(borderwidth=1, highlightthickness=1, highlightbackground="black")
piano = Piano(root)

# Inicia el bucle de eventos de la ventana  
piano.run()
