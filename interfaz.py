import tkinter as tk
from tkinter import font

class EkoUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EKO - Interfaz Visual")
        self.geometry("400x700")
        self.configure(bg="#ffffff")
        self.frames = {}
        for F in (LoginScreen, MainScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)
        self.show_frame(LoginScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# ---------- Pantalla de inicio de sesión ----------
class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#ffffff")
        tk.Label(self, text="EKO", font=("Helvetica", 36, "bold"), fg="#008542", bg="white").pack(pady=60)
        tk.Label(self, text="Número de celular", bg="white").pack(pady=(0, 5))
        self.user = tk.Entry(self, font=("Helvetica", 14), width=30)
        self.user.pack(pady=5)

        tk.Label(self, text="PIN", bg="white").pack(pady=(20, 5))
        self.password = tk.Entry(self, font=("Helvetica", 14), width=30, show="*")
        self.password.pack(pady=5)

        tk.Button(self, text="Ingresar", bg="#008542", fg="white",
                  font=("Helvetica", 14, "bold"), width=20,
                  command=lambda: master.show_frame(MainScreen)).pack(pady=40)

# ---------- Pantalla principal tipo EKO ----------
class MainScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#F5F5F5")
        header = tk.Frame(self, bg="#008542", height=120)
        header.pack(fill="x")
        tk.Label(header, text="Hola, Laura 👋", bg="#008542", fg="white", font=("Helvetica", 16)).place(x=20, y=20)
        tk.Label(header, text="Saldo disponible", bg="#008542", fg="white", font=("Helvetica", 12)).place(x=20, y=60)
        tk.Label(header, text="Gs. 2.300.000", bg="#008542", fg="white", font=("Helvetica", 22, "bold")).place(x=20, y=85)

        container = tk.Frame(self, bg="#F5F5F5")
        container.pack(pady=30)

        self.big_button(container, "📤 Enviar dinero")
        self.big_button(container, "💡 Pagar servicios")
        self.big_button(container, "📄 Movimientos")
        self.big_button(container, "🏧 Extraer efectivo")
        self.big_button(container, "💳 Configurar tarjeta")

        tk.Button(self, text="🔒 Cerrar sesión", font=("Helvetica", 12),
                  bg="#CCCCCC", command=lambda: master.show_frame(LoginScreen)).pack(pady=40)

    def big_button(self, parent, text):
        tk.Button(parent, text=text, font=("Helvetica", 14), width=30,
                  height=2, bg="white", relief="groove").pack(pady=10)

# Ejecutar interfaz
if __name__ == "__main__":
    app = EkoUI()
    app.mainloop()