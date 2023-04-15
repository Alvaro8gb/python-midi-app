import tkinter as tk

# Define las dimensiones de la ventana y el tamaño de cada tecla  
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
KEY_WIDTH = WINDOW_WIDTH // 14
KEY_HEIGHT = int(WINDOW_HEIGHT * 0.75)

# Define la lista de colores de las teclas  
KEY_COLORS = ["white", "black", "white", "black", "white", "white", "black",
              "white", "black", "white", "black", "white", "white", "black",
              "white"]

class Piano:
    def __init__(self, master):
        # Crea el lienzo en el que se dibujarán las teclas  
        self.canvas = tk.Canvas(master, width=WINDOW_WIDTH,
                                height=WINDOW_HEIGHT)
        self.canvas.pack()

        # Crea los botones para cada tecla y los almacena en una lista  
        self.buttons = []
        for i in range(len(KEY_COLORS)):
            x = i * KEY_WIDTH
            y = 0
            color = KEY_COLORS[i]
            button = tk.Button(self.canvas, bg=color, activebackground=color,
                               borderwidth=0, highlightthickness=0,
                               command=lambda i=i: self.on_button_pressed(i))
            button.place(x=x, y=y, width=KEY_WIDTH, height=KEY_HEIGHT)
            self.buttons.append(button)

    def on_button_pressed(self, index):
        # Cambia el color del botón cuando se presiona  
        button = self.buttons[index]
        button.config(bg="red", activebackground="red")

    def run(self):
        # Inicia el bucle de eventos de la ventana  
        tk.mainloop()

    # Crea una ventana y un objeto Piano


root = tk.Tk()
root.title("Piano Digital")
piano = Piano(root)

# Inicia el bucle de eventos de la ventana  
piano.run()
