# programa python en repositorio mejorado
import tkinter as tk

ventana = tk.Tk()
ventana.title("Programa para subir a repositorio")
ventana.geometry("500x250")  # más ancho para que no se recorte
ventana.config(bg="#1e1e2f")

etiqueta = tk.Label(
    ventana,
    text="Este programa es de Marquez y Peñaloza",
    font=("Helvetica", 16, "bold"),
    fg="red",
    bg="#1e1e2f",
    wraplength=450,   # evita que el texto se salga de la ventana
    justify="center"  # centra el texto si ocupa varias líneas
)

# Centrado perfecto en la ventana
etiqueta.place(relx=0.5, rely=0.5, anchor="center")

ventana.mainloop()
