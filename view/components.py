import tkinter as tk


COLOR_LABEL = "#FFE5E1"
class Key:
    def __init__(self, canvas, color, status, key_width, key_height):
        self.status = status
        self.canvas = canvas
        self.button = tk.Button(self.canvas, bg=color, activebackground=color,
                                borderwidth=1, highlightthickness=3, highlightbackground="black")

        self.label = tk.Label(self.canvas, text="", bg=COLOR_LABEL)

        self.key_width = key_width
        self.key_height = key_height

    def place(self, x, y):
        self.button.place(x=x, y=y, width=self.key_width, height=self.key_height)
        self.label.place(x=x + 17, y=y + self.key_height)


class PopupWindow:
    def __init__(self, master, message):
        self.master = master
        self.message = message

        # Crear ventana emergente
        self.popup_window = tk.Toplevel(master)
        self.popup_window.title("Modelo finalizado")
        self.popup_window.geometry("300x100")
        self.popup_window.resizable(False, False)

        # Crear etiqueta con el mensaje
        self.label = tk.Label(self.popup_window, text=message)
        self.label.pack(pady=10)

        # Crear botón para cerrar la ventana
        self.close_button = tk.Button(self.popup_window, text="Cerrar", command=self.popup_window.destroy)
        self.close_button.pack(pady=10)

    def center(self):
        # Centrar la ventana emergente en la pantalla principal
        self.master.update_idletasks()
        width = self.popup_window.winfo_width()
        height = self.popup_window.winfo_height()
        x = (self.master.winfo_width() // 2) - (width // 2)
        y = (self.master.winfo_height() // 2) - (height // 2)
        self.popup_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def create_modal_window(root, title):
    """
    Crear vetana modal para elegir parametros
    """
    window = tk.Toplevel()

    window.title(title)

    ancho_ventana = 400
    altura_ventana = 100
    x = root.winfo_x() + (root.winfo_width() - ancho_ventana) // 2
    y = root.winfo_y() + (root.winfo_height() - altura_ventana) // 2
    window.geometry(f"{ancho_ventana}x{altura_ventana}+{x}+{y}")

    return window
