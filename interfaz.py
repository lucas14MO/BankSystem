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
                  ProyeccionesFrame, ConsideracionesFrame,
                  NuevoDepositoFrame, NuevaExtraccionFrame, NuevoChequeFrame):
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
        self.tree.bind("<Double-1>", self.seleccionar_banco)
        self.tree_visible = False  # Para rastrear si el treeview está visible

        tk.Button(self, text="Ingresar", font=("Helvetica", 14),
                  bg="#007C4A", fg="white", command=self.validar_manual).pack(pady=10)

    def actualizar_sugerencias(self, event=None):
        texto = self.entry.get().lower().strip()
        coincidencias = [b for b in self.master.bancos if texto in b.lower()]

        if texto and coincidencias:
            if not self.tree_visible:
                self.tree.pack(pady=10, padx=20, fill="x")
                self.tree_visible = True
            self.tree.delete(*self.tree.get_children())
            for banco in coincidencias:
                self.tree.insert("", "end", values=(banco,))
        else:
            if self.tree_visible:
                self.tree.pack_forget()
                self.tree_visible = False

    def seleccionar_banco(self, event):
        item = self.tree.focus()
        if item:
            banco = self.tree.item(item)["values"][0]
            self.master.banco_seleccionado.set(banco)
            self.master.show_frame(MenuPrincipalFrame)

    def validar_manual(self):
        banco_ingresado = self.entry.get().strip()
        if banco_ingresado in self.master.bancos:
            self.master.banco_seleccionado.set(banco_ingresado)
            self.master.show_frame(MenuPrincipalFrame)
        else:
            item = self.tree.focus()
            if item:
                banco = self.tree.item(item)["values"][0]
                self.master.banco_seleccionado.set(banco)
                self.master.show_frame(MenuPrincipalFrame)
            else:
                messagebox.showerror("Error", "Debe seleccionar o ingresar un banco válido.")

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
        tk.Label(self, text="📂 Cuentas Bancarias", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        # Filtros y búsqueda
        filtro_frame = tk.Frame(self, bg="#F8FFF8")
        filtro_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(filtro_frame, text="Filtrar por tipo:", font=("Helvetica", 12),
                 bg="#F8FFF8").pack(side="left", padx=(0, 10))

        self.filtro_tipo = ttk.Combobox(filtro_frame, values=["Todos", "Corriente", "Caja Ahorro"], state="readonly")
        self.filtro_tipo.set("Todos")
        self.filtro_tipo.pack(side="left")
        self.filtro_tipo.bind("<<ComboboxSelected>>", self.filtrar_cuentas)

        # Tabla
        columnas = ["N° Cuenta", "Tipo", "Saldo", "Límite"]
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=8)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")

        self.tabla.pack(pady=10, padx=20, fill="both", expand=True)

        # Datos simulados
        self.datos_cuentas = [
            ("001-123", "Corriente", "2.000.000", "1.000.000"),
            ("002-456", "Caja Ahorro", "850.000", "0"),
            ("003-789", "Corriente", "3.500.000", "1.500.000"),
            ("004-321", "Caja Ahorro", "650.000", "0")
        ]
        self.mostrar_cuentas(self.datos_cuentas)

        # Indicadores visuales
        self.total_label = tk.Label(self, text="", font=("Helvetica", 12, "italic"), bg="#F8FFF8")
        self.total_label.pack(pady=5)
        self.actualizar_resumen()

        # Acciones
        acciones_frame = tk.Frame(self, bg="#F8FFF8")
        acciones_frame.pack(pady=10)

        tk.Button(acciones_frame, text="➕ Agregar nueva cuenta", bg="#007C4A", fg="white", width=22).pack(side="left", padx=10)
        tk.Button(acciones_frame, text="🔍 Ver detalles", bg="white", width=15).pack(side="left", padx=10)

        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=15)

    def mostrar_cuentas(self, lista):
        self.tabla.delete(*self.tabla.get_children())
        for c in lista:
            self.tabla.insert("", "end", values=c)

    def filtrar_cuentas(self, event=None):
        tipo = self.filtro_tipo.get()
        if tipo == "Todos":
            self.mostrar_cuentas(self.datos_cuentas)
        else:
            filtradas = [c for c in self.datos_cuentas if c[1] == tipo]
            self.mostrar_cuentas(filtradas)
        self.actualizar_resumen()

    def actualizar_resumen(self):
        total = 0
        for item in self.tabla.get_children():
            saldo_str = self.tabla.item(item)["values"][2]
            try:
                saldo = int(saldo_str.replace(".", "").replace(",", ""))
                total += saldo
            except:
                pass
        cuentas_mostradas = len(self.tabla.get_children())
        self.total_label.config(text=f"Total de cuentas: {cuentas_mostradas} | Saldo acumulado: {total:,} Gs.".replace(",", "."))

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

        tk.Button(self, text="➕ Registrar nuevo cheque", bg="#4CAF50", fg="white",
                  command=lambda: master.show_frame(NuevoChequeFrame)).pack(pady=5)
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

        tk.Button(self, text="➕ Hacer nuevo depósito", bg="#4CAF50", fg="white",
                  command=lambda: master.show_frame(NuevoDepositoFrame)).pack(pady=5)
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

        tk.Button(self, text="➕ Hacer nueva extracción", bg="#4CAF50", fg="white",
                  command=lambda: master.show_frame(NuevaExtraccionFrame)).pack(pady=5)
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


# ----------------------- Formularios adicionales ----------------------- #

class NuevoDepositoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Nuevo Depósito", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        tk.Label(self, text="Cuenta:", font=("Helvetica", 14), bg="#F8FFF8").pack(pady=10)
        self.cuenta_entry = tk.Entry(self, font=("Helvetica", 14))
        self.cuenta_entry.pack()

        tk.Label(self, text="Monto:", font=("Helvetica", 14), bg="#F8FFF8").pack(pady=10)
        self.monto_entry = tk.Entry(self, font=("Helvetica", 14))
        self.monto_entry.pack()

        tk.Label(self, text="Fecha:", font=("Helvetica", 14), bg="#F8FFF8").pack(pady=10)
        self.fecha_entry = tk.Entry(self, font=("Helvetica", 14))
        self.fecha_entry.pack()

        tk.Button(self, text="Guardar Depósito", bg="#007C4A", fg="white",
                  command=self.guardar_deposito).pack(pady=20)

        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(DepositosFrame)).pack()

    def guardar_deposito(self):
        cuenta = self.cuenta_entry.get()
        monto = self.monto_entry.get()
        fecha = self.fecha_entry.get()
        messagebox.showinfo("Depósito registrado", f"Depósito guardado:\nCuenta: {cuenta}\nMonto: {monto}\nFecha: {fecha}")
        self.master.show_frame(DepositosFrame)


class NuevaExtraccionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Nueva Extracción", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        tk.Label(self, text="Cuenta:", font=("Helvetica", 14), bg="#F8FFF8").pack(pady=10)
        self.cuenta_entry = tk.Entry(self, font=("Helvetica", 14))
        self.cuenta_entry.pack()

        tk.Label(self, text="Monto:", font=("Helvetica", 14), bg="#F8FFF8").pack(pady=10)
        self.monto_entry = tk.Entry(self, font=("Helvetica", 14))
        self.monto_entry.pack()

        tk.Label(self, text="Fecha:", font=("Helvetica", 14), bg="#F8FFF8").pack(pady=10)
        self.fecha_entry = tk.Entry(self, font=("Helvetica", 14))
        self.fecha_entry.pack()

        tk.Button(self, text="Guardar Extracción", bg="#007C4A", fg="white",
                  command=self.guardar_extraccion).pack(pady=20)

        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(ExtraccionesFrame)).pack()

    def guardar_extraccion(self):
        cuenta = self.cuenta_entry.get()
        monto = self.monto_entry.get()
        fecha = self.fecha_entry.get()
        messagebox.showinfo("Extracción registrada", f"Extracción guardada:\nCuenta: {cuenta}\nMonto: {monto}\nFecha: {fecha}")
        self.master.show_frame(ExtraccionesFrame)


class NuevoChequeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Registrar nuevo Cheque", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        tk.Label(self, text="Tipo (A la vista / Diferido / Rechazado):", font=("Helvetica", 14), bg="#F8FFF8").pack(pady=10)
        self.tipo_entry = tk.Entry(self, font=("Helvetica", 14))
        self.tipo_entry.pack()

        tk.Label(self, text="Número:", font=("Helvetica", 14), bg="#F8FFF8").pack(pady=10)
        self.numero_entry = tk.Entry(self, font=("Helvetica", 14))
        self.numero_entry.pack()

        tk.Label(self, text="Monto:", font=("Helvetica", 14), bg="#F8FFF8").pack(pady=10)
        self.monto_entry = tk.Entry(self, font=("Helvetica", 14))
        self.monto_entry.pack()

        tk.Button(self, text="Guardar Cheque", bg="#007C4A", fg="white",
                  command=self.guardar_cheque).pack(pady=20)

        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(ChequesFrame)).pack()

    def guardar_cheque(self):
        tipo = self.tipo_entry.get()
        numero = self.numero_entry.get()
        monto = self.monto_entry.get()
        messagebox.showinfo("Cheque registrado", f"Cheque guardado:\nTipo: {tipo}\nNúmero: {numero}\nMonto: {monto}")
        self.master.show_frame(ChequesFrame)


# --------------------------- EJECUCIÓN --------------------------- #
if __name__ == "__main__":
    app = BancoApp()
    app.mainloop()