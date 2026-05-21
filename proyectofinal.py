import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Punto de Venta")
ventana.geometry("500x600")
ventana.configure(bg="black")
ventana.resizable(False, False)

# -------------------------
# LOGO (AQUÍ VA BIEN COLOCADO)
# -------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_logo = os.path.join(BASE_DIR, "logo.png")

    imagen = Image.open(ruta_logo)
    imagen = imagen.resize((250, 250))
    img_logo = ImageTk.PhotoImage(imagen)

    lbl_logo = tk.Label(ventana, image=img_logo, bg="black")
    lbl_logo.image = img_logo
    lbl_logo.pack(pady=10)

except:
    tk.Label(
        ventana,
        text="(Aquí va el logo)",
        bg="black",
        fg="white",
        font=("Arial", 14)
    ).pack(pady=20)

# -------------------------
# REGISTRO PRODUCTOS
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

        messagebox.showinfo("OK", "Guardado")

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

# -------------------------
# REGISTRO VENTAS
# -------------------------
def abrir_registro_ventas():
    ven = tk.Toplevel()
    ven.title("Ventas")
    ven.geometry("420x450")
    ven.configure(bg="black")

    productos = {}

    try:
        path = os.path.join(os.path.dirname(__file__), "productos.txt")
        with open(path, "r", encoding="utf-8") as f:
            for l in f:
                p = l.strip().split("|")
                if len(p) == 4:
                    productos[p[1]] = float(p[2])
    except:
        messagebox.showerror("Error", "No hay productos")
        ven.destroy()
        return

    def lbl(t): return tk.Label(ven, text=t, bg="black", fg="white")

    lbl("Producto").pack()
    cb = ttk.Combobox(ven, values=list(productos.keys()), state="readonly")
    cb.pack()

    lbl("Precio").pack()
    txt_p = tk.Entry(ven, state="readonly"); txt_p.pack()

    lbl("Cantidad").pack()
    txt_c = tk.Entry(ven); txt_c.pack()

    lbl("Total").pack()
    txt_t = tk.Entry(ven, state="readonly"); txt_t.pack()

    def calc(*a):
        try:
            total = float(txt_p.get()) * int(txt_c.get())
            txt_t.config(state="normal")
            txt_t.delete(0, tk.END)
            txt_t.insert(0, str(total))
            txt_t.config(state="readonly")
        except:
            pass

    def sel(event):
        prod = cb.get()
        txt_p.config(state="normal")
        txt_p.delete(0, tk.END)
        txt_p.insert(0, productos.get(prod, 0))
        txt_p.config(state="readonly")
        calc()

    def guardar():
        if not cb.get() or not txt_p.get() or not txt_c.get():
            messagebox.showwarning("Error", "Completa todo")
            return

        path = os.path.join(os.path.dirname(__file__), "ventas.txt")
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{cb.get()}|{txt_p.get()}|{txt_c.get()}|{txt_t.get()}\n")

        messagebox.showinfo("OK", "Venta guardada")

        cb.set("")
        txt_p.config(state="normal"); txt_p.delete(0, tk.END); txt_p.config(state="readonly")
        txt_c.delete(0, tk.END)
        txt_t.config(state="normal"); txt_t.delete(0, tk.END); txt_t.config(state="readonly")

    cb.bind("<<ComboboxSelected>>", sel)
    txt_c.bind("<KeyRelease>", calc)

    tk.Button(
        ven,
        text="Registrar Venta",
        command=guardar,
        bg="#39FF14",
        fg="black",
        font=("Arial", 12, "bold"),
        width=20,
        height=2,
        bd=0
    ).pack(pady=20)

# -------------------------
# BOTONES PRINCIPALES
# -------------------------
def boton(texto, cmd):
    return tk.Button(
        ventana,
        text=texto,
        command=cmd,
        bg="#39FF14",
        fg="black",
        font=("Arial", 12, "bold"),
        width=25,
        height=2,
        bd=0
    )

boton("Registro de Productos", abrir_registro_productos).pack(pady=10)
boton("Registro de Ventas", abrir_registro_ventas).pack(pady=10)
boton("Reportes", lambda: messagebox.showinfo("Info", "En construcción")).pack(pady=10)
boton("Acerca de", lambda: messagebox.showinfo("Info", "Punto de Venta de Ropa\nProyecto Escolar\nVersión 1.0")).pack(pady=10)

ventana.mainloop()