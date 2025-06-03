
import tkinter as tk
from tkinter import ttk, messagebox

class BancoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Bancario Visual")
        self.geometry("800x600")
        self.configure(bg="#E6F0EA")
        self.bancos = ["Banco Familiar", "Banco Continental", "Visión Banco"]
        self.banco_seleccionado = tk.StringVar(value="")

        self.frames = {}
        for F in (SeleccionBancoFrame, MenuPrincipalFrame, BancosFrame, CuentasFrame,
                  ChequesFrame, DepositosFrame, ExtraccionesFrame,
                  ProyeccionesFrame, ConsideracionesFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(SeleccionBancoFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class SeleccionBancoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        tk.Label(self, text="Seleccione un banco", font=("Helvetica", 18, "bold"),
                 bg="white", fg="#007C4A").pack(pady=20)

        self.entry = tk.Entry(self, font=("Helvetica", 14))
        self.entry.pack(pady=10, ipadx=10, padx=20, fill="x")
        self.entry.bind("<KeyRelease>", self.actualizar_sugerencias)

        self.tree = ttk.Treeview(self, columns=("Banco"), show="headings", height=5)
        self.tree.heading("Banco", text="Bancos disponibles")
        self.tree.pack(pady=10, padx=20, fill="x")
        self.tree.bind("<Double-1>", self.seleccionar_banco)

        tk.Button(self, text="Ingresar", font=("Helvetica", 14),
                  bg="#007C4A", fg="white", command=self.validar_manual).pack(pady=10)

        self.actualizar_sugerencias()

    def actualizar_sugerencias(self, event=None):
        texto = self.entry.get().lower().strip()
        self.tree.delete(*self.tree.get_children())
        if texto:
            for banco in self.master.bancos:
                if texto in banco.lower():
                    self.tree.insert("", "end", values=(banco,))

    def seleccionar_banco(self, event):
        item = self.tree.focus()
        if item:
            banco = self.tree.item(item)["values"][0]
            self.master.banco_seleccionado.set(banco)
            self.master.show_frame(MenuPrincipalFrame)

    def validar_manual(self):
        banco = self.entry.get().strip()
        if banco in self.master.bancos:
            self.master.banco_seleccionado.set(banco)
            self.master.show_frame(MenuPrincipalFrame)
        else:
            messagebox.showerror("Error", "Debe seleccionar un banco válido.")


class MenuPrincipalFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#E6F0EA")
        tk.Label(self, text="Menú Principal", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        self.info_banco = tk.Label(self, text="", font=("Helvetica", 14), bg="#E6F0EA")
        self.info_banco.pack(pady=10)

        opciones = [
            ("Bancos", BancosFrame),
            ("Cuentas", CuentasFrame),
            ("Cheques", ChequesFrame),
            ("Depósitos", DepositosFrame),
            ("Extracciones", ExtraccionesFrame),
            ("Proyecciones", ProyeccionesFrame),
            ("Consideraciones", ConsideracionesFrame)
        ]
        for nombre, frame in opciones:
            tk.Button(self, text=nombre, font=("Helvetica", 14),
                      bg="white", width=30, height=2,
                      command=lambda f=frame: master.show_frame(f)).pack(pady=5)

        tk.Button(self, text="Cambiar banco", bg="#CCCCCC",
                  command=lambda: master.show_frame(SeleccionBancoFrame)).pack(pady=10)

    def tkraise(self, *args, **kwargs):
        banco = self.master.banco_seleccionado.get()
        self.info_banco.config(text=f"Banco seleccionado: {banco}")
        super().tkraise(*args, **kwargs)


class BancosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Listado de Bancos", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        self.lista = tk.Listbox(self, font=("Helvetica", 12))
        self.lista.pack(pady=10, padx=20, fill="both", expand=True)
        self.actualizar_lista()

        self.entry = tk.Entry(self, font=("Helvetica", 12))
        self.entry.pack(pady=5, padx=20, fill="x")

        tk.Button(self, text="Agregar banco", bg="#007C4A", fg="white",
                  command=self.agregar_banco).pack(pady=5)

        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=10)

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        for banco in self.master.bancos:
            self.lista.insert(tk.END, banco)

    def agregar_banco(self):
        nuevo = self.entry.get().strip()
        if nuevo and nuevo not in self.master.bancos:
            self.master.bancos.append(nuevo)
            self.entry.delete(0, tk.END)
            self.actualizar_lista()


class CuentasFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Cuentas", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        cuentas = [("001-123", "Corriente", "2.000.000", "1.000.000"),
                   ("002-456", "Caja Ahorro", "850.000", "0")]

        columnas = ["N° Cuenta", "Tipo", "Saldo", "Límite"]
        tabla = ttk.Treeview(self, columns=columnas, show="headings", height=6)
        for col in columnas:
            tabla.heading(col, text=col)
        for c in cuentas:
            tabla.insert("", "end", values=c)
        tabla.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Button(self, text="Transferir entre cuentas", bg="#007C4A", fg="white").pack(pady=5)
        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=10)


class ChequesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Cheques (a la vista, diferidos, rechazados)", font=("Helvetica", 16, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        datos = [("A la vista", "001", "1.000.000"),
                 ("Diferido", "002", "2.500.000"),
                 ("Rechazado", "003", "500.000")]
        columnas = ["Tipo", "N°", "Monto"]
        tabla = ttk.Treeview(self, columns=columnas, show="headings", height=6)
        for col in columnas:
            tabla.heading(col, text=col)
        for d in datos:
            tabla.insert("", "end", values=d)
        tabla.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=10)


class DepositosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Depósitos", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        tk.Label(self, text="Monto: 1.500.000 Gs.", font=("Helvetica", 14),
                 bg="#F8FFF8").pack(pady=10)
        tk.Label(self, text="Fecha: 01/06/2025", font=("Helvetica", 14),
                 bg="#F8FFF8").pack(pady=5)
        tk.Label(self, text="Cuenta: 001-123", font=("Helvetica", 14),
                 bg="#F8FFF8").pack(pady=5)

        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=20)


class ExtraccionesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Extracciones", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        tk.Label(self, text="Monto: 800.000 Gs.", font=("Helvetica", 14),
                 bg="#F8FFF8").pack(pady=10)
        tk.Label(self, text="Fecha: 02/06/2025", font=("Helvetica", 14),
                 bg="#F8FFF8").pack(pady=5)
        tk.Label(self, text="Cuenta: 002-456", font=("Helvetica", 14),
                 bg="#F8FFF8").pack(pady=5)

        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=20)


class ProyeccionesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Proyecciones", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")
        tk.Label(self, text="Proyección de saldo para el próximo mes: 3.200.000 Gs.",
                 font=("Helvetica", 14), bg="#F8FFF8").pack(pady=30)
        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=20)


class ConsideracionesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Consideraciones", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")
        consideraciones = [
            "✔ Las cuentas pueden tener sobregiro",
            "✔ Se permiten transferencias entre cuentas",
            "✔ Se registra cada cheque rechazado"
        ]
        for c in consideraciones:
            tk.Label(self, text=c, font=("Helvetica", 14), bg="#F8FFF8", anchor="w").pack(pady=10, padx=20)
        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=20)


# --------------------------- EJECUCIÓN --------------------------- #
if __name__ == "__main__":
    app = BancoApp()
    app.mainloop()