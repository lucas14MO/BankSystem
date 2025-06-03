import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from doctest import master
from tkinter import ttk, messagebox

from decimal import *

from sqlalchemy import false

import main
from main import *


class BancoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Bancario Visual")
        self.geometry("800x600")
        self.configure(bg="#E6F0EA")
        self.banco_seleccionado = tk.StringVar(value="")

        self.frames = {}
        for F in (SeleccionBancoFrame, MenuPrincipalFrame, BancosFrame, CuentasFrame,
                  ChequesFrame, Transacciones, ExtraccionesFrame,
                  ProyeccionesFrame, ConsideracionesFrame,
                  NuevoDepositoFrame, NuevaExtraccionFrame, NuevoChequeFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(SeleccionBancoFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.on_frame_change()
        frame.tkraise()


class SeleccionBancoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.session = Session()  # Crea su propia sesión de base de datos
        self.tree_visible = False

        # Título
        tk.Label(self, text="Seleccione un banco", font=("Helvetica", 18, "bold"),
                 bg="white", fg="#007C4A").pack(pady=20)

        # Campo de entrada
        self.entry = tk.Entry(self, font=("Helvetica", 14), fg="grey")
        self.entry.insert(0, "Ingrese el nombre del banco...")
        self.entry.bind("<FocusIn>", self.limpiar_placeholder)
        self.entry.bind("<FocusOut>", self.restaurar_placeholder)
        self.entry.bind("<KeyRelease>", self.actualizar_sugerencias)
        self.entry.pack(pady=10, ipadx=10, padx=20, fill="x")

        # Árbol de resultados
        self.tree = ttk.Treeview(self, columns=("Banco",), show="headings", height=5)
        self.tree.heading("Banco", text="Bancos disponibles")
        self.tree.bind("<Double-1>", self.seleccionar_banco)

        # Botón para ingresar manualmente
        tk.Button(self, text="Ingresar", font=("Helvetica", 14),
                  bg="#007C4A", fg="white", command=self.validar_manual).pack(pady=10)

    def limpiar_placeholder(self, event):
        if self.entry.get() == "Ingrese el nombre del banco...":
            self.entry.delete(0, tk.END)
            self.entry.config(fg="black")

    def restaurar_placeholder(self, event):
        if not self.entry.get().strip():
            self.entry.insert(0, "Ingrese el nombre del banco...")
            self.entry.config(fg="grey")

    def actualizar_sugerencias(self, event=None):
        texto = self.entry.get().lower().strip()
        if texto == "ingrese el nombre del banco...":
            return

        bancos = self.session.query(Bank).all()
        coincidencias = [b.name_bank for b in bancos if texto in b.name_bank.lower()]

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
        if banco_ingresado.lower() == "ingrese el nombre del banco...":
            messagebox.showerror("Error", "Debe ingresar o seleccionar un banco válido.")
            return

        banco_bd = self.session.query(Bank).filter_by(name_bank=banco_ingresado).first()

        if banco_bd:
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

    def on_frame_change(self):
        print("Cambio de frame: Selección de Banco")

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
            ("Transacciones", Transacciones)
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

    def on_frame_change(self):
        print("Cambio de frame: Menu principal!")

class BancosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        self.master = master
        self.session = Session()

        # Encabezado
        tk.Label(self, text="🏦 Listado de Bancos", font=("Helvetica", 20, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        # Contenedor principal
        contenedor = tk.Frame(self, bg="#E6F2EC")
        contenedor.pack(fill="both", expand=True, padx=40, pady=20)

        # Frame tipo tarjeta para lista
        card = tk.Frame(contenedor, bg="white", bd=2, relief="groove")
        card.pack(fill="both", expand=True, side="left", padx=(0, 20), pady=10)

        tk.Label(card, text="📋 Bancos registrados", font=("Helvetica", 14, "bold"),
                 bg="white", fg="#333").pack(pady=10)

        self.lista = tk.Listbox(card, font=("Helvetica", 12), bg="white", bd=0, highlightthickness=0)
        self.lista.pack(pady=5, padx=10, fill="both", expand=True)

        # Frame para agregar banco
        form = tk.Frame(contenedor, bg="#E6F2EC")
        form.pack(side="right", fill="y", expand=False)

        tk.Label(form, text="➕ Agregar nuevo banco", font=("Helvetica", 14, "bold"),
                 bg="#E6F2EC", fg="#007C4A").pack(pady=10)

        # Nombre
        self.nombre_entry = tk.Entry(form, font=("Helvetica", 12), fg="grey")
        self.nombre_entry.insert(0, "Nombre del nuevo banco")
        self.nombre_entry.bind("<FocusIn>", lambda e: self.limpiar_placeholder(self.nombre_entry, "Nombre del nuevo banco"))
        self.nombre_entry.bind("<FocusOut>", lambda e: self.restaurar_placeholder(self.nombre_entry, "Nombre del nuevo banco"))
        self.nombre_entry.pack(pady=5, padx=5, fill="x")

        # Teléfono
        self.tel_entry = tk.Entry(form, font=("Helvetica", 12), fg="grey")
        self.tel_entry.insert(0, "Teléfono de contacto")
        self.tel_entry.bind("<FocusIn>", lambda e: self.limpiar_placeholder(self.tel_entry, "Teléfono de contacto"))
        self.tel_entry.bind("<FocusOut>", lambda e: self.restaurar_placeholder(self.tel_entry, "Teléfono de contacto"))
        self.tel_entry.pack(pady=5, padx=5, fill="x")

        # Botón Agregar
        tk.Button(form, text="✅ Agregar banco", font=("Helvetica", 12),
                  bg="#007C4A", fg="white", command=self.agregar_banco).pack(pady=10, fill="x", padx=5)

        # Botón Volver
        tk.Button(form, text="⬅ Volver al menú", font=("Helvetica", 12),
                  bg="#CCCCCC", command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=20, fill="x", padx=5)

        self.actualizar_lista()

    def limpiar_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def restaurar_placeholder(self, entry, placeholder):
        if not entry.get().strip():
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        bancos = self.session.query(Bank).order_by(Bank.name_bank.asc()).all()
        for banco in bancos:
            self.lista.insert(tk.END, f"{banco.name_bank} - {banco.phone_bank}")

    def agregar_banco(self):
        nombre = self.nombre_entry.get().strip()
        telefono = self.tel_entry.get().strip()

        if nombre.lower() == "nombre del nuevo banco" or not nombre:
            messagebox.showwarning("Aviso", "Debe ingresar un nombre válido para el banco.")
            return
        if telefono.lower() == "teléfono de contacto" or not telefono:
            messagebox.showwarning("Aviso", "Debe ingresar un número de teléfono válido.")
            return

        # Verificar existencia
        existe = self.session.query(Bank).filter(Bank.name_bank.ilike(nombre)).first()
        if existe:
            messagebox.showinfo("Ya existe", "Este banco ya está registrado.")
            return

        # Crear y guardar
        nuevo_banco = Bank(name_bank=nombre, phone_bank=telefono)
        self.session.add(nuevo_banco)
        self.session.commit()

        # Limpiar
        self.nombre_entry.delete(0, tk.END)
        self.tel_entry.delete(0, tk.END)
        self.restaurar_placeholder(self.nombre_entry, "Nombre del nuevo banco")
        self.restaurar_placeholder(self.tel_entry, "Teléfono de contacto")

        # Actualizar lista
        self.actualizar_lista()

    def on_frame_change(self):
        print("Cambio de frame: Lista de Bancos")
        self.actualizar_lista()

class CuentasFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="📂 Cuentas Bancarias", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")
        self.master = master
        # Filtros y búsqueda
        filtro_frame = tk.Frame(self, bg="#F8FFF8")
        filtro_frame.pack(pady=10, padx=20, fill="x")

        # Tabla
        columnas = ["N° Cuenta", "Nombres", "Apellidos", "Saldo", "Telefono"]
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=8)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center")

        self.tabla.pack(pady=10, padx=20, fill="both", expand=True)

        # Indicadores visuales
        self.total_label = tk.Label(self, text="", font=("Helvetica", 12, "italic"), bg="#F8FFF8")
        self.total_label.pack(pady=5)

        # Acciones
        acciones_frame = tk.Frame(self, bg="#F8FFF8")
        acciones_frame.pack(pady=10)

        tk.Button(acciones_frame, text="➕ Agregar nueva cuenta", bg="#007C4A", fg="white", width=22).pack(side="left", padx=10)
        tk.Button(acciones_frame, text="🔍 Ver detalles", bg="white", width=15, command=self.detalle_cuenta).pack(side="left", padx=10)

        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=15)

    def mostrar_cuentas(self):
        self.tabla.delete(*self.tabla.get_children())

        banco = self.master.banco_seleccionado.get()
        id_banco = get_bank_by_name(banco).id_bank
        cuentas = get_account_from_bank(id_banco)
        if cuentas:
            for cuenta in cuentas:

                self.tabla.insert("", "end", values=[
                    cuenta.number_account, cuenta.name_account, cuenta.lastname_account, cuenta.balance_account, cuenta.phone_account
                ])


    def actualizar_resumen(self):
        total = Decimal("0.00")
        for item in self.tabla.get_children():
            saldo_str = self.tabla.item(item)["values"][3]
            saldo = Decimal(saldo_str)
            total += saldo

        cuentas_mostradas = len(self.tabla.get_children())
        self.total_label.config(text=f"Total de cuentas: {cuentas_mostradas} | Saldo acumulado: {total:,} Gs.".replace(",", "."))

    def detalle_cuenta(self):
        acc_number = int(self.tabla.item(self.tabla.selection()[0], 'values')[0])

        ventana_detalle = tk.Toplevel(self)  # Crea una nueva ventana independiente
        ventana_detalle.title(f"Detalles de la cuenta {acc_number}")

        frame = DetalleCuenta(ventana_detalle, acc_number)  # Asigna el frame a la nueva ventana
        frame.pack(fill="both", expand=True)  # Ajusta la visibilidad del frame en la nueva ventana

    def on_frame_change(self):
        self.mostrar_cuentas()
        self.actualizar_resumen()



class DetalleCuenta(tk.Frame):
    def __init__(self, master, numero_cuenta):
        super().__init__(master, bg="#F0F8F5")
        self.master = master

        # Obtener datos de la cuenta
        cuenta = get_account_by_acc_number(numero_cuenta)
        if not cuenta:
            messagebox.showerror("Error", "Cuenta no encontrada.")
            return

        # Frame estilo tarjeta
        tarjeta = tk.Frame(self, bg="white", bd=2, relief="groove")
        tarjeta.pack(pady=40, padx=40, ipadx=10, ipady=10)

        # Título
        tk.Label(tarjeta, text="Detalles de la Cuenta", font=("Helvetica", 16, "bold"),
                 bg="white", fg="#007C4A").grid(row=0, column=0, columnspan=2, pady=10)

        # Diccionario de campos
        datos = {
            "Pais Documento": get_nationality_by_id(cuenta.id_nationality).country_nationality,
            "Número de Cuenta": cuenta.number_account,
            "Cédula": cuenta.ci_account,
            "Nombres": cuenta.name_account,
            "Apellidos": cuenta.lastname_account,
            "Teléfono": cuenta.phone_account,
            "Dirección": cuenta.address_account,
            "Saldo": f"{cuenta.balance_account:,.2f} Gs",
            "Faltas": cuenta.faults_account
        }

        # Mostrar cada campo como fila
        for idx, (campo, valor) in enumerate(datos.items(), start=1):
            color_valor = "#28A745" if campo == "Saldo" else "black"
            font_valor = ("Helvetica", 12, "bold") if campo == "Saldo" else ("Helvetica", 12)

            tk.Label(tarjeta, text=f"{campo}:", anchor="w",
                     font=("Helvetica", 12), bg="white", width=18).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            tk.Label(tarjeta, text=valor, anchor="w",
                     font=font_valor, fg=color_valor, bg="white").grid(row=idx, column=1, sticky="w", padx=10, pady=5)

class ChequesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F5F5F5")

        # Encabezado superior
        header = tk.Label(self, text="📄 Cheques emitidos", font=("Helvetica", 20, "bold"),
                          bg="#2C7865", fg="white", pady=15)
        header.pack(fill="x")

        # Contenedor principal
        contenido = tk.Frame(self, bg="#F5F5F5")
        contenido.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame tipo tarjeta para tabla
        tabla_card = tk.Frame(contenido, bg="white", bd=1, relief="solid")
        tabla_card.pack(fill="both", expand=True, pady=10)

        # Tabla de cheques
        columnas = ["Emisor", "Receptor", "Diferido", "Monto", "Fecha Emisión", "Fecha Vencimiento", "Estado"]
        self.tabla = ttk.Treeview(tabla_card, columns=columnas, show="headings", height=10)

        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        estilo.configure("Treeview", font=("Helvetica", 10), rowheight=28)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=110)

        self.tabla.pack(padx=10, pady=10, fill="both", expand=True)

        # Controles de filtro y cantidad
        control_frame = tk.Frame(contenido, bg="#F5F5F5")
        control_frame.pack(fill="x", pady=10)

        tk.Label(control_frame, text="Filtrar por estado:", font=("Helvetica", 11), bg="#F5F5F5").pack(side="left", padx=(5, 5))
        self.combo_estado = ttk.Combobox(control_frame, state="readonly", width=15)
        self.combo_estado.pack(side="left")
        self.combo_estado.bind("<<ComboboxSelected>>", self.actualizar_tabla)

        self.label_cantidad = tk.Label(control_frame, text="Total cheques: 0", font=("Helvetica", 11), bg="#F5F5F5")
        self.label_cantidad.pack(side="right", padx=10)

        # Botones de acción
        botones = tk.Frame(self, bg="#F5F5F5")
        botones.pack(pady=10)

        btn_registrar = tk.Button(botones, text="➕ Registrar nuevo cheque", bg="#4CAF50", fg="white",
                                  font=("Helvetica", 11, "bold"), padx=10, pady=6, relief="flat",
                                  command=lambda: master.show_frame(NuevoChequeFrame))
        btn_registrar.pack(side="left", padx=10)

        btn_volver = tk.Button(botones, text="⬅ Volver al menú", bg="#D9D9D9", font=("Helvetica", 11),
                               padx=10, pady=6, relief="flat",
                               command=lambda: master.show_frame(MenuPrincipalFrame))
        btn_volver.pack(side="left", padx=10)

    def on_frame_change(self):
        nombre_banco = self.master.banco_seleccionado.get()
        id_banco = get_bank_by_name(nombre_banco).id_bank

        estados = [estado.state_cheque for estado in session.query(ChequeState).all()]
        self.combo_estado["values"] = ["Todos"] + estados
        self.combo_estado.set("Todos")

        self.actualizar_tabla()

    def actualizar_tabla(self, event=None):
        estado_seleccionado = self.combo_estado.get()
        nombre_banco = self.master.banco_seleccionado.get()
        id_banco = get_bank_by_name(nombre_banco).id_bank
        cheques = get_cheque_from_bank(id_banco)

        self.tabla.delete(*self.tabla.get_children())

        cheques_filtrados = []
        if cheques:
            for cheque in cheques:
                cheque_fmt = ChequeFormated(cheque)
                if estado_seleccionado == "Todos" or cheque_fmt.cheque_state == estado_seleccionado:
                    cheques_filtrados.append(cheque_fmt)

            for chq in cheques_filtrados:
                self.tabla.insert("", "end", values=[
                    chq.emitter_account.name_account,
                    chq.receptor_account.name_account if chq.receptor_account else "Al portador",
                    "No" if chq.is_deferred_cheque == 0 else "Sí",
                    chq.payment_cheque,
                    chq.pushDate_cheque,
                    chq.endDate_cheque,
                    chq.cheque_state
                ])

        self.label_cantidad.config(text=f"Total cheques: {len(cheques_filtrados)}")


class Transacciones(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Transacciones Realizadas", font=("Helvetica", 16, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")

        columnas = ["Emisor", "Receptor", "Monto", "Fecha Transaccion"]
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=6)
        for col in columnas:
            self.tabla.heading(col, text=col)
        self.tabla.pack(pady=10, padx=10, fill="both", expand=True)

    def on_frame_change(self):
        nombre_banco = self.master.banco_seleccionado.get()
        id_banco = get_bank_by_name(nombre_banco).id_bank

        transacciones = get_transactions_from_bank(id_banco)
        if transacciones:
            for transaccion in transacciones:
                tra_formated = TransactionFormated(transaccion)
                self.tabla.insert("", "end", values=[
                    f"{tra_formated.emitter_account.number_account}:{tra_formated.emitter_account.name_account}",
                    f"{tra_formated.receptor_account.number_account}:{tra_formated.receptor_account.name_account}",
                    tra_formated.amount_transaction,
                    tra_formated.date_transaction
                ])

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

    def on_frame_change(self):
        print("Cambio de frame!")

class ProyeccionesFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F8FFF8")
        tk.Label(self, text="Proyecciones", font=("Helvetica", 18, "bold"),
                 bg="#007C4A", fg="white", height=2).pack(fill="x")
        tk.Label(self, text="Proyección de saldo para el próximo mes: 3.200.000 Gs.",
                 font=("Helvetica", 14), bg="#F8FFF8").pack(pady=30)
        tk.Button(self, text="⬅ Volver", bg="#CCCCCC",
                  command=lambda: master.show_frame(MenuPrincipalFrame)).pack(pady=20)

    def on_frame_change(self):
        print("Cambio de frame!")

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

    def on_frame_change(self):
        print("Cambio de frame!")

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
                  command=lambda: master.show_frame(Transacciones)).pack()

    def guardar_deposito(self):
        cuenta = self.cuenta_entry.get()
        monto = self.monto_entry.get()
        fecha = self.fecha_entry.get()
        messagebox.showinfo("Depósito registrado", f"Depósito guardado:\nCuenta: {cuenta}\nMonto: {monto}\nFecha: {fecha}")
        self.master.show_frame(Transacciones)

    def on_frame_change(self):
        print("Cambio de frame!")

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

    def on_frame_change(self):
        print("Cambio de frame!")

class NuevoChequeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F5F5F5")

        # Título superior
        tk.Label(self, text="📝 Registrar nuevo Cheque", font=("Helvetica", 20, "bold"),
                 bg="#2C7865", fg="white", pady=15).pack(fill="x")

        self.accounts = None
        self.id_banco = -1

        # Contenedor central tipo tarjeta
        form_card = tk.Frame(self, bg="white", bd=1, relief="solid")
        form_card.pack(padx=30, pady=20, fill="both", expand=True)

        def add_labeled_entry(parent, label_text, var_attr, is_date=False):
            tk.Label(parent, text=label_text, font=("Helvetica", 13, "bold"), bg="white", anchor="w").pack(fill="x", padx=20, pady=(12, 2))
            if is_date:
                entry = DateEntry(parent, font=("Helvetica", 13), background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
            else:
                entry = tk.Entry(parent, font=("Helvetica", 13), bg="#FAFAFA", relief="groove", bd=1)
            entry.pack(padx=20, fill="x", pady=(0, 5))
            setattr(self, var_attr, entry)

        # Campos

        add_labeled_entry(form_card, "Número Cuenta Emisor:", "nro_emisor")
        # Dentro de tu clase o función de interfaz
        self.banco_receptor_cb = ttk.Combobox(self, state="readonly", width=40)
        self.banco_receptor_cb.pack(pady=10)
        self.banco_receptor_cb.bind("<<ComboboxSelected>>", self.banco_receptor_seleccionado)
        add_labeled_entry(form_card, "Número Cuenta Receptor (Dejar en blanco para dejar al portador):", "nro_receptor")

        # Diferido
        tk.Label(form_card, text="¿Es Cheque Diferido? (Si el cheque no es diferido, la fecha de fin no se tomara en cuenta)", font=("Helvetica", 13, "bold"), bg="white", anchor="w").pack(fill="x", padx=20, pady=(12, 2))
        self.esDiferido = tk.BooleanVar(value=False)

        radio_frame = tk.Frame(form_card, bg="white")
        radio_frame.pack(fill="x", padx=20)

        tk.Radiobutton(radio_frame, text="Sí", variable=self.esDiferido, value=True,
                       font=("Helvetica", 12), bg="white").pack(side="left", padx=10)
        tk.Radiobutton(radio_frame, text="No", variable=self.esDiferido, value=False,
                       font=("Helvetica", 12), bg="white").pack(side="left", padx=10)

        add_labeled_entry(form_card, "Fecha de Emisión:", "fecha_inicio", is_date=True)
        add_labeled_entry(form_card, "Fecha de Vencimiento:", "fecha_fin", is_date=True)
        add_labeled_entry(form_card, "Monto:", "monto_entry")

        # Botones
        btn_frame = tk.Frame(form_card, bg="white")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Guardar Cheque", bg="#4CAF50", fg="white",
                  font=("Helvetica", 12, "bold"), padx=10, pady=6, relief="flat",
                  command=self.guardar_cheque).pack(side="left", padx=10)

        tk.Button(btn_frame, text="⬅ Volver", bg="#D9D9D9", fg="black",
                  font=("Helvetica", 12), padx=10, pady=6, relief="flat",
                  command=lambda: master.show_frame(ChequesFrame)).pack(side="left", padx=10)
        
        # Crear Listbox para sugerencias, inicialmente oculto
        self.lb_suggestions = tk.Listbox(self, height=5, font=("Helvetica", 12), bg="white", relief="solid", bd=1)
        self.lb_suggestions.place_forget()  # Oculto al inicio

        # Función para mostrar sugerencias
        def show_suggestions(event):
            typed = self.nro_emisor.get().strip()
            if not typed or not self.accounts:
                self.lb_suggestions.place_forget()
                return

            # Filtrar cuentas que empiezan con typed (como string)
            filtered = [str(acc.number_account) for acc in self.accounts if str(acc.number_account).startswith(typed)]

            if filtered:
                self.lb_suggestions.delete(0, tk.END)
                for item in filtered:
                    self.lb_suggestions.insert(tk.END, item)

                # Posicionar el listbox justo abajo del entry
                x = self.nro_emisor.winfo_rootx() - self.winfo_rootx()
                y = self.nro_emisor.winfo_rooty() - self.winfo_rooty() + self.nro_emisor.winfo_height()
                width = self.nro_emisor.winfo_width()
                self.lb_suggestions.place(x=x, y=y, width=width)
            else:
                self.lb_suggestions.place_forget()

        # Función para elegir sugerencia y ponerla en el entry
        def on_select_suggestion(event):
            selection = self.lb_suggestions.curselection()
            if selection:
                picked = self.lb_suggestions.get(selection[0])
                self.nro_emisor.delete(0, tk.END)
                self.nro_emisor.insert(0, picked)
                self.lb_suggestions.place_forget()

        # Vincular eventos
        self.nro_emisor.bind("<KeyRelease>", show_suggestions)
        self.lb_suggestions.bind("<<ListboxSelect>>", on_select_suggestion)

        # Para ocultar la lista si clickeás fuera
        def hide_suggestions(event):
            if event.widget != self.lb_suggestions and event.widget != self.nro_emisor:
                self.lb_suggestions.place_forget()

        self.bind_all("<Button-1>", hide_suggestions)   
    def banco_receptor_seleccionado(self, event):
        nombre_banco = self.banco_receptor_cb.get().strip()
        if not nombre_banco:
            return

        # Buscar el banco por nombre
        banco = session.query(Bank).filter(Bank.name_bank == nombre_banco).first()
        if not banco:
            messagebox.showerror("Error", "No se encontró el banco seleccionado.")
            return

        # Obtener todas las cuentas asociadas a ese banco
        cuentas = session.query(Account).filter(Account.id_bank == banco.id_bank).all()

        if not cuentas:
            messagebox.showinfo("Sin cuentas", "Este banco no tiene cuentas registradas.")
            self.receptor_cuenta_cb['values'] = []
            return

        # Preparar valores para mostrar: "Número - Nombre Apellido"
        cuentas_mostrar = [
            f"{cuenta.number_account} - {cuenta.name_account or ''} {cuenta.lastname_account or ''}".strip()
            for cuenta in cuentas
        ]

        # Rellenar el combobox de cuentas receptoras
        self.receptor_cuenta_cb['values'] = cuentas_mostrar
        self.receptor_cuenta_cb.set('')  # Limpiar selección anterior si había
    def cargar_bancos_receptores(self):
        bancos = session.query(Bank).order_by(Bank.name_bank).all()
        nombres_bancos = [b.name_bank for b in bancos]

        self.banco_receptor_cb['values'] = nombres_bancos
        if nombres_bancos:
            self.banco_receptor_cb.set('')  # Limpia selección anterior
    def guardar_cheque(self):
        nro_emisor = self.nro_emisor.get().strip()
        nro_receptor = self.nro_receptor.get().strip()
        fecha_in = self.fecha_inicio.get_date()
        fecha_fi = self.fecha_fin.get_date()
        monto_raw = self.monto_entry.get().strip()
        diferido = 1 if self.esDiferido.get() else 0

        # Validación básica
        if not nro_emisor or not fecha_in or not monto_raw:
            messagebox.showwarning("Campos incompletos", "Debe completar al menos: emisor, fecha y monto.")
            return

        # Calcular fecha fin
        if diferido == 0:
            fecha_fi = fecha_in + timedelta(days=30)
        else:
            max_fecha_fi = fecha_in + timedelta(days=180)
            if fecha_fi > max_fecha_fi:
                messagebox.showerror("Fecha inválida", "La fecha de vencimiento no puede ser más de 180 días después de la fecha de emisión.")
                return

        # Validar monto
        try:
            monto = Decimal(monto_raw)
            if monto <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messagebox.showerror("Monto inválido", "Ingrese un monto válido y mayor que cero.")
            return

        # Validar cuentas
        try:
            nro_emisor_int = int(nro_emisor)
        except ValueError:
            messagebox.showerror("Cuenta emisora inválida", "El número de cuenta emisora debe ser un entero.")
            return

        try:
            nro_receptor_int = int(nro_receptor) if nro_receptor else None
        except ValueError:
            messagebox.showerror("Cuenta receptora inválida", "El número de cuenta receptora debe ser un entero.")
            return

        # Verificar cuenta emisora
        ac_emisor_q = session.query(Account).filter(
            Account.number_account == nro_emisor_int,
            Account.id_bank == self.id_banco
        )

        if ac_emisor_q.count() == 0:
            messagebox.showerror("Cuenta emisora no encontrada", "No se encontró la cuenta emisora en este banco.")
            return

        ac_emisor = ac_emisor_q.one()

        # Verificar cuenta receptora (si hay)
        ac_receptor = None
        if nro_receptor_int:
            ac_receptor_q = session.query(Account).filter(Account.number_account == nro_receptor_int)
            if ac_receptor_q.count() == 0:
                messagebox.showerror("Cuenta receptora no encontrada", "No se encontró la cuenta receptora.")
                return
            ac_receptor = ac_receptor_q.one()

        # Determinar estado del cheque
        if diferido == 1:
            id_cheque_state = 1  # vigente
        else:
            if ac_emisor.balance_account is not None and ac_emisor.balance_account >= monto:
                id_cheque_state = 1  # vigente
            else:
                id_cheque_state = 2  # rechazado

        # Registrar cheque
        add_cheque(
            id_emitter_account=ac_emisor.id_account,
            id_receptor_account=ac_receptor.id_account if ac_receptor else None,
            payment=monto,
            push_date=fecha_in.strftime("%Y-%m-%d"),
            end_date=fecha_fi.strftime("%Y-%m-%d"),
            address=ac_emisor.address_account,
            is_deferred=diferido,
            id_cheque_state=id_cheque_state
        )

        messagebox.showinfo("Éxito", f"Cheque registrado como {'vigente' if id_cheque_state == 1 else 'rechazado'}.")
        self.master.show_frame(ChequesFrame)

       

    def on_frame_change(self):
        nombre_banco = self.master.banco_seleccionado.get()
        self.id_banco = get_bank_by_name(nombre_banco).id_bank
        self.accounts = get_account_from_bank(self.id_banco)
        

# --------------------------- EJECUCIÓN --------------------------- #
if __name__ == "__main__":
    #Crear referencia a la base de datos
    DATABASE_URL = "mysql+pymysql://root@localhost/banksystem"
    engine = create_engine(DATABASE_URL)

    #Coneccion a la base de datos
    Session = sessionmaker(bind=engine)
    session = Session()
    main.session = session

    #UI
    app = BancoApp()
    app.mainloop()