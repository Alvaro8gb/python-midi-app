import tkinter as tk
import tkinter.messagebox as messagebox

from globals import CHUNK_SIZE, MODELS
from view.components import Key, PopupWindow, create_modal_window

# Diseño vetana piano
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
KEY_WIDTH = WINDOW_WIDTH // 14
KEY_HEIGHT = int(WINDOW_HEIGHT * 0.75)
COLOR_PRESSED = "#ADD8E6"
KEY_COLORS = ("white", "black", "white", "black", "white", "white", "black",
              "white", "black", "white", "black", "white")


midi2chord = dict([(0, 'C'), (1, 'C#'), (2, 'D'), (3, 'D#'),
                   (4, 'E'), (5, 'F'), (6, 'F#'), (7, 'G'),
                   (8, 'G#'), (9, 'A'), (10, 'A#'), (11, 'B')])


class Interface(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Python-midi-app")
        # Cargar el archivo de imagen desde el disco.
        icono = tk.PhotoImage(file="view/icono.png")
        # Establecerlo como ícono de la ventana.
        self.iconphoto(True, icono)
        self.controller = controller
        self.input_device = None
        self.midi_devices = controller.get_midi_devices()
        # Piano
        self.piano = tk.Canvas(self, width=650, height=WINDOW_HEIGHT)
        self.resizable(False, False)
        
        self.piano.pack()
        self.spinbox = tk.Spinbox(self.piano, values=[str(size) for size in CHUNK_SIZE], width=10,
                                  command=self.on_spinbox_change, state='readonly')
        self.spinbox.place(x=540, y=70)
        # Keys
        self.keys = self.__create_keys__()

        # Selector midi device
        self.midi_device_selection = None
        connect_button = tk.Button(self.piano, text="Conectar MIDI", command=self.window_select_midi)
        connect_button.place(x=540, y=0)

        # Selector modelo
        self.model_selection = self.controller.get_model_name()
        mode_button = tk.Button(self.piano, text="Modelo", command=self.window_select_model)
        mode_button.place(x=540, y=100)

        # Selector tamaño chunk
        tk.Label(self.piano, text="chunk:", bg="white").place(x=540, y=40)

        # Configurar cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Centrar ventana principal
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = WINDOW_WIDTH + 80
        height = WINDOW_HEIGHT + 20
        # Calcular las coordenadas de la ventana para que se centre en la pantalla
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Configurar la posición de la ventana en la pantalla
        self.geometry('{}x{}+{}+{}'.format(650, WINDOW_HEIGHT, x, y))

    def __create_keys__(self):
        """
        Crea los botones para cada tecla y los almacena en una lista
        """
        keys = {}

        for i in range(len(KEY_COLORS)):
            x = i * KEY_WIDTH+25
            y = 0
            color = KEY_COLORS[i]
            keys[i] = Key(self.piano, color, False, KEY_WIDTH, KEY_HEIGHT)
            keys[i].place(x, y)

        return keys

    def run(self):
        """
         Inicia el bucle de eventos de la ventana
        """

        try:

            self.mainloop()

        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(error_message)
            self.show_pop_up(error_message)

    def show_pop_up(self, msg):
        popup = PopupWindow(self, msg)
        popup.center()
        self.wait_window(popup.popup_window)

    def window_select_midi(self):

        if len(self.midi_devices) == 0:
            messagebox.showerror("Error", "No se encontraron dispositivos MIDI")
        else:
            window = create_modal_window(self, "Seleciona conector")
            etiqueta = tk.Label(window, text="Selecciona una opción:")
            etiqueta.pack()
            selection = tk.StringVar(value=self.midi_devices[0])
            desplegable = tk.OptionMenu(window, selection, *self.midi_devices)
            desplegable.pack()

            boton_confirmar = tk.Button(window, text="Confirmar",
                                        command=lambda: self.confirm_midi(window, selection))
            boton_confirmar.pack()

    def confirm_midi(self, window, selection):
        if self.input_device != None:
            self.controller.disconect_midi_device()

        self.input_device = selection.get()
        self.controller.connect_midi_device(self.input_device)

        print("Teclado MIDI conectado ", self.input_device)
        window.destroy()

    def window_select_model(self):
        window = create_modal_window(self, "Seleccionado Modelo")

        etiqueta = tk.Label(window, text="Selecciona un modelo:")
        etiqueta.pack()

        model_selection = tk.StringVar(value=self.model_selection)

        desplegable = tk.OptionMenu(window, model_selection, *MODELS)
        desplegable.pack()

        boton_confirmar = tk.Button(window, text="Confirmar",
                                    command=lambda: self.confirm_model(window, model_selection))
        boton_confirmar.pack()

    def confirm_model(self, window, model_selection):
        model = model_selection.get()

        self.controller.change_model(model)

        print("Modelo seleccionado: ", model)

        self.model_selection = model

        window.destroy()

    def on_spinbox_change(self):

        chunk_size = self.spinbox.get()
        print("Spinbox value changed:", chunk_size)

        self.controller.change_chunk(chunk_size)

    def press_key(self, note):
        """

        Cambia el color del botón cuando se presiona

        """
        index = note % 12
        key = self.keys[index]

        if not key.status:
            key.status = True
            key.button.config(bg=COLOR_PRESSED, activebackground=COLOR_PRESSED)
            key.label.config(text=self.midi_to_chord(note))

    def release_key(self, note):
        """

        Restaurar tecla
        """

        index = note % 12
        key = self.keys[index]

        if key.status:
            key.status = False
            key.button.config(bg=KEY_COLORS[index], activebackground=KEY_COLORS[index])
            key.label.config(text="")

    def on_closing(self):
        if tk.messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
            self.controller.end()
            self.destroy()

    @staticmethod
    def midi_to_chord(midi_note):
        # Obtener el número de tono y el número de octava
        tone = midi_note % 12
        octave = midi_note // 12 - 1
        # Obtener el símbolo de acorde correspondiente
        chord_symbol = midi2chord[tone]
        # Agregar el número de octava al símbolo de acorde
        chord_notation = f'{chord_symbol}{octave}'

        return chord_notation
