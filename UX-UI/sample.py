import tkinter as tk
  
# Crear la ventana principal  
root = tk.Tk()  
root.title("Interfaz de usuario")  
  
# Crear el menú de configuración  
menu_bar = tk.Menu(root)  
root.config(menu=menu_bar)  
  
# Crear el menú desplegable "Archivo"  
file_menu = tk.Menu(menu_bar, tearoff=0)  
file_menu.add_command(label="Abrir")  
file_menu.add_command(label="Guardar")  
file_menu.add_separator()  
file_menu.add_command(label="Salir", command=root.quit)  
menu_bar.add_cascade(label="Archivo", menu=file_menu)  
  
# Crear el menú desplegable "Configuración"  
settings_menu = tk.Menu(menu_bar, tearoff=0)  
settings_menu.add_command(label="Opción 1")  
settings_menu.add_command(label="Opción 2")  
menu_bar.add_cascade(label="Configuración", menu=settings_menu)  
  
# Crear el teclado en la parte inferior  
keyboard_frame = tk.Frame(root)  
keyboard_frame.pack(side=tk.BOTTOM)  
  
# Crear los botones del teclado  
button_1 = tk.Button(keyboard_frame, text="1")  
button_2 = tk.Button(keyboard_frame, text="2")  
button_3 = tk.Button(keyboard_frame, text="3")  
button_4 = tk.Button(keyboard_frame, text="4")  
button_5 = tk.Button(keyboard_frame, text="5")  
button_6 = tk.Button(keyboard_frame, text="6")  
button_7 = tk.Button(keyboard_frame, text="7")  
button_8 = tk.Button(keyboard_frame, text="8")  
button_9 = tk.Button(keyboard_frame, text="9")  
button_0 = tk.Button(keyboard_frame, text="0")  
button_1.pack(side=tk.LEFT)  
button_2.pack(side=tk.LEFT)  
button_3.pack(side=tk.LEFT)  
button_4.pack(side=tk.LEFT)  
button_5.pack(side=tk.LEFT)  
button_6.pack(side=tk.LEFT)  
button_7.pack(side=tk.LEFT)  
button_8.pack(side=tk.LEFT)  
button_9.pack(side=tk.LEFT)  
button_0.pack(side=tk.LEFT)  
  
# Iniciar el bucle principal de la aplicación  
root.mainloop()  
