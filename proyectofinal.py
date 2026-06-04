import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
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
# LOGO
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
# PRODUCTOS
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

# -------------------------
# VENTAS + TICKET
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

    # CALCULAR
    def calc(*a):
        try:
            total = float(txt_p.get()) * int(txt_c.get())

            txt_t.config(state="normal")
            txt_t.delete(0, tk.END)
            txt_t.insert(0, str(total))
            txt_t.config(state="readonly")
        except:
            pass

    # SELECCIÓN
    def sel(event):
        prod = cb.get()

        txt_p.config(state="normal")
        txt_p.delete(0, tk.END)
        txt_p.insert(0, str(productos.get(prod, 0)))
        txt_p.config(state="readonly")

        calc()

    # TICKET
    def mostrar_ticket(producto, precio, cantidad, total):
        ticket = tk.Toplevel()
        ticket.title("Ticket")
        ticket.geometry("300x350")
        ticket.configure(bg="black")

        fecha = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

        texto = (
            " *** PUNTO DE VENTA ***\n"
            "--------------------------\n"
            f"Fecha: {fecha}\n"
            "--------------------------\n"
            f"Producto: {producto}\n"
            f"Precio: ${precio}\n"
            f"Cantidad: {cantidad}\n"
            "--------------------------\n"
            f"TOTAL: ${total}\n"
            "--------------------------\n"
            " ¡GRACIAS POR SU COMPRA!"
        )

        tk.Label(
            ticket,
            text=texto,
            font=("Consolas", 11),
            bg="black",
            fg="white",
            justify="left"
        ).pack(pady=15)

        tk.Button(
            ticket,
            text="Cerrar",
            command=ticket.destroy,
            bg="#39FF14",
            fg="black",
            font=("Arial", 10, "bold"),
            bd=0
        ).pack(pady=10)

    # GUARDAR VENTA
    def guardar():
        if not cb.get() or not txt_p.get() or not txt_c.get():
            messagebox.showwarning("Error", "Completa todo")
            return

        prod = cb.get()
        precio = txt_p.get()
        cant = txt_c.get()
        total = txt_t.get()

        path = os.path.join(os.path.dirname(__file__), "ventas.txt")
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{prod}|{precio}|{cant}|{total}\n")

        messagebox.showinfo("Venta Registrada", "La venta se registró correctamente.")

        mostrar_ticket(prod, precio, cant, total)

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
# REPORTES
# -------------------------
def abrir_reportes():
    ventana_r = tk.Toplevel()
    ventana_r.title("Reporte de Ventas")
    ventana_r.geometry("700x450")
    ventana_r.configure(bg="black")

    tk.Label(
        ventana_r,
        text="REPORTE DE VENTAS",
        font=("Arial", 16, "bold"),
        bg="black",
        fg="#39FF14"
    ).pack(pady=10)

    frame = tk.Frame(ventana_r, bg="black")
    frame.pack()

    columnas = ("producto", "precio", "cantidad", "total")

    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=15)

    tabla.heading("producto", text="Producto")
    tabla.heading("precio", text="Precio")
    tabla.heading("cantidad", text="Cantidad")
    tabla.heading("total", text="Total")

    tabla.column("producto", width=250, anchor="center")
    tabla.column("precio", width=100, anchor="center")
    tabla.column("cantidad", width=100, anchor="center")
    tabla.column("total", width=120, anchor="center")

    tabla.pack()

    try:
        path = os.path.join(os.path.dirname(__file__), "ventas.txt")
        with open(path, "r", encoding="utf-8") as f:
            for l in f:
                if l.strip():
                    tabla.insert("", tk.END, values=l.strip().split("|"))
    except:
        messagebox.showerror("Error", "No hay ventas")

    tk.Button(
        ventana_r,
        text="Cerrar",
        command=ventana_r.destroy,
        bg="#39FF14",
        fg="black",
        font=("Arial", 12, "bold"),
        width=15,
        height=2,
        bd=0
    ).pack(pady=10)

# -------------------------
# BOTONES PRINCIPALES
# -------------------------
def boton(t, c):
    return tk.Button(
        ventana,
        text=t,
        command=c,
        bg="#39FF14",
        fg="black",
        font=("Arial", 12, "bold"),
        width=25,
        height=2,
        bd=0
    )

boton("Registro de Productos", abrir_registro_productos).pack(pady=10)
boton("Registro de Ventas", abrir_registro_ventas).pack(pady=10)
boton("Reportes", abrir_reportes).pack(pady=10)
boton("Acerca de", lambda: messagebox.showinfo("Info", "Punto de Venta de Ropa\nProyecto Escolar\nVersión 1.0")).pack(pady=10)

ventana.mainloop()