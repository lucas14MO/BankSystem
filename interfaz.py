import tkinter as tk
from tkinter import ttk

# Ventana principal
root = tk.Tk()
root.title("Sistema Bancario")
root.geometry("800x600")

# Pestañas
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# ==== BANCO ====
banco_frame = ttk.Frame(notebook)
notebook.add(banco_frame, text="Bancos")

# Banco - Widgets
label_banco = ttk.Label(banco_frame, text="Nombre del Banco:")
label_banco.pack(pady=10)
entry_banco = ttk.Entry(banco_frame, width=50)
entry_banco.pack(pady=5)

label_tel_banco = ttk.Label(banco_frame, text="Teléfono:")
label_tel_banco.pack(pady=10)
entry_tel_banco = ttk.Entry(banco_frame, width=50)
entry_tel_banco.pack(pady=5)

# ==== CUENTA ====
cuenta_frame = ttk.Frame(notebook)
notebook.add(cuenta_frame, text="Cuentas")

label_nombre = ttk.Label(cuenta_frame, text="Nombre:")
label_nombre.pack(pady=10)
entry_nombre = ttk.Entry(cuenta_frame, width=50)
entry_nombre.pack(pady=5)

label_apellido = ttk.Label(cuenta_frame, text="Apellido:")
label_apellido.pack(pady=10)
entry_apellido = ttk.Entry(cuenta_frame, width=50)
entry_apellido.pack(pady=5)

label_cedula = ttk.Label(cuenta_frame, text="Cédula:")
label_cedula.pack(pady=10)
entry_cedula = ttk.Entry(cuenta_frame, width=50)
entry_cedula.pack(pady=5)

label_telefono = ttk.Label(cuenta_frame, text="Teléfono:")
label_telefono.pack(pady=10)
entry_telefono = ttk.Entry(cuenta_frame, width=50)
entry_telefono.pack(pady=5)

label_direccion = ttk.Label(cuenta_frame, text="Dirección:")
label_direccion.pack(pady=10)
entry_direccion = ttk.Entry(cuenta_frame, width=50)
entry_direccion.pack(pady=5)

# ==== CHEQUE ====
cheque_frame = ttk.Frame(notebook)
notebook.add(cheque_frame, text="Cheques")

label_emisor = ttk.Label(cheque_frame, text="Cuenta Emisora:")
label_emisor.pack(pady=10)
entry_emisor = ttk.Entry(cheque_frame, width=50)
entry_emisor.pack(pady=5)

label_receptor = ttk.Label(cheque_frame, text="Cuenta Receptora:")
label_receptor.pack(pady=10)
entry_receptor = ttk.Entry(cheque_frame, width=50)
entry_receptor.pack(pady=5)

label_monto = ttk.Label(cheque_frame, text="Monto:")
label_monto.pack(pady=10)
entry_monto = ttk.Entry(cheque_frame, width=50)
entry_monto.pack(pady=5)

label_fecha_emision = ttk.Label(cheque_frame, text="Fecha de Emisión:")
label_fecha_emision.pack(pady=10)
entry_fecha_emision = ttk.Entry(cheque_frame, width=50)
entry_fecha_emision.pack(pady=5)

label_fecha_venc = ttk.Label(cheque_frame, text="Fecha de Vencimiento:")
label_fecha_venc.pack(pady=10)
entry_fecha_venc = ttk.Entry(cheque_frame, width=50)
entry_fecha_venc.pack(pady=5)

label_direccion_pago = ttk.Label(cheque_frame, text="Dirección de Pago:")
label_direccion_pago.pack(pady=10)
entry_direccion_pago = ttk.Entry(cheque_frame, width=50)
entry_direccion_pago.pack(pady=5)

root.mainloop()