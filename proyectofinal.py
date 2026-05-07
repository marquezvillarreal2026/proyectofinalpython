import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# -------------------------
# FUNCIONES
# -------------------------
def abrir_registro_productos():
    reg = tk.Toplevel()
    reg.title("Productos")
    reg.geometry("400x420")
    reg.configure(bg="black")

    def lbl(t): return tk.Label(reg, text=t, bg="black", fg="white")

    lbl("ID").pack()
    idp = tk.Entry(reg); idp.pack()

    lbl("Descripción").pack()
    desc = tk.Entry(reg); desc.pack()

    lbl("Precio").pack()
    precio = tk.Entry(reg); precio.pack()

    lbl("Categoría").pack()
    cat = tk.Entry(reg); cat.pack()

    def guardar():
        if not idp.get() or not desc.get() or not precio.get() or not cat.get():
            messagebox.showwarning("Error", "Completa todo")
            return

        try:
            float(precio.get())
        except:
            messagebox.showerror("Error", "Precio inválido")
            return

        path = os.path.join(os.path.dirname(__file__), "productos.txt")
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{idp.get()}|{desc.get()}|{precio.get()}|{cat.get()}\n")

        messagebox.showinfo("OK", "Producto guardado")

        idp.delete(0, tk.END)
        desc.delete(0, tk.END)
        precio.delete(0, tk.END)
        cat.delete(0, tk.END)

    tk.Button(
        reg,
        text="Guardar",
        command=guardar,
        bg="#39FF14",
        fg="black",
        font=("Arial", 12, "bold"),
        width=20,
        height=2,
        bd=0
    ).pack(pady=20)

def abrir_registro_ventas():
    messagebox.showinfo("Ventas", "Aquí irá el módulo de ventas.")


def abrir_reportes():
    messagebox.showinfo("Reportes", "Aquí irá el módulo de reportes.")


def abrir_acerca_de():
    messagebox.showinfo("Acerca de", "Punto de Venta de Ropa\nProyecto Escolar\nVersión 1.0")


# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Punto de Venta - Ropa")
ventana.geometry("500x600")
ventana.resizable(False, False)
ventana.configure(bg="black")

# -------------------------
# LOGO
# -------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    imagen = Image.open(os.path.join(BASE_DIR, "logo.png"))
    imagen = imagen.resize((250, 250))
    img_logo = ImageTk.PhotoImage(imagen)

    tk.Label(ventana, image=img_logo, bg="black").pack(pady=20)
except:
    tk.Label(
        ventana,
        text="(Aquí va el logo del sistema)",
        font=("Arial", 14),
        bg="black",
        fg="white"
    ).pack(pady=40)

# -------------------------
# BOTONES
# -------------------------
def crear_boton(texto, comando):
    return tk.Button(
        ventana,
        text=texto,
        command=comando,
        font=("Arial", 12, "bold"),
        bg="#39FF14",
        fg="black",
        activebackground="#00cc00",
        activeforeground="white",
        width=25,
        height=2,
        bd=0
    )

crear_boton("Registro de Productos", abrir_registro_productos).pack(pady=10)
crear_boton("Registro de Ventas", abrir_registro_ventas).pack(pady=10)
crear_boton("Reportes", abrir_reportes).pack(pady=10)
crear_boton("Acerca de", abrir_acerca_de).pack(pady=10)

# -------------------------
# INICIO
# -------------------------
ventana.mainloop()