import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class EkoUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EKO - Interfaz Visual")
        self.geometry("400x700")
        self.resizable(False, False)

        self.frames = {}
        for F in (LoginScreen, MainScreen, AccountScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(LoginScreen)

    def show_frame(self, screen):
        self.frames[screen].tkraise()

# ---------- Pantalla de inicio de sesión ----------
class LoginScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="EKO", font=ctk.CTkFont(size=36, weight="bold"), text_color="#008542").pack(pady=60)

        ctk.CTkLabel(self, text="Número de celular").pack(pady=(0, 5))
        self.user_entry = ctk.CTkEntry(self, placeholder_text="Ej: 0981 123 456")
        self.user_entry.pack(pady=5, padx=40)

        ctk.CTkLabel(self, text="PIN").pack(pady=(20, 5))
        self.password_entry = ctk.CTkEntry(self, placeholder_text="PIN", show="*")
        self.password_entry.pack(pady=5, padx=40)

        ctk.CTkButton(self, text="Ingresar", fg_color="#008542", hover_color="#006f36",
                      command=lambda: master.show_frame(MainScreen)).pack(pady=40)

# ---------- Pantalla principal ----------
class MainScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        header = ctk.CTkFrame(self, fg_color="#008542", height=140)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Hola, Laura 👋", font=ctk.CTkFont(size=18), text_color="white").place(x=20, y=20)
        ctk.CTkLabel(header, text="Saldo disponible", font=ctk.CTkFont(size=14), text_color="white").place(x=20, y=60)
        ctk.CTkLabel(header, text="Gs. 2.300.000", font=ctk.CTkFont(size=22, weight="bold"), text_color="white").place(x=20, y=85)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(pady=30, fill="x")

        self.big_button(container, "📤 Enviar dinero")
        self.big_button(container, "💡 Pagar servicios")
        self.big_button(container, "📄 Movimientos")
        self.big_button(container, "🏧 Extraer efectivo")
        self.big_button(container, "👤 Ver cuentas", command=lambda: master.show_frame(AccountScreen))

        ctk.CTkButton(self, text="🔒 Cerrar sesión", fg_color="#CCCCCC", text_color="black", hover_color="#AAAAAA",
                      command=lambda: master.show_frame(LoginScreen)).pack(pady=40)

    def big_button(self, parent, text, command=None):
        ctk.CTkButton(parent, text=text, width=300, height=45,
                      fg_color="white", text_color="black",
                      hover_color="#f0f0f0", corner_radius=8,
                      command=command).pack(pady=10)

# ---------- Pantalla visual de la tabla account ----------
import customtkinter as ctk

import customtkinter as ctk

class AccountScreen(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        title = ctk.CTkLabel(self, text="Información de la Cuenta", font=ctk.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Labels manuales sin usar bucles
        self.label_bank = ctk.CTkLabel(self, text="Banco:")
        self.value_bank = ctk.CTkLabel(self, text="")

        self.label_nationality = ctk.CTkLabel(self, text="Nacionalidad:")
        self.value_nationality = ctk.CTkLabel(self, text="")

        self.label_number_account = ctk.CTkLabel(self, text="Número de Cuenta:")
        self.value_number_account = ctk.CTkLabel(self, text="")

        self.label_ci = ctk.CTkLabel(self, text="C.I.:")
        self.value_ci = ctk.CTkLabel(self, text="")

        self.label_name = ctk.CTkLabel(self, text="Nombre:")
        self.value_name = ctk.CTkLabel(self, text="")

        self.label_lastname = ctk.CTkLabel(self, text="Apellido:")
        self.value_lastname = ctk.CTkLabel(self, text="")

        self.label_phone = ctk.CTkLabel(self, text="Teléfono:")
        self.value_phone = ctk.CTkLabel(self, text="")

        self.label_address = ctk.CTkLabel(self, text="Dirección:")
        self.value_address = ctk.CTkLabel(self, text="")

        self.label_balance = ctk.CTkLabel(self, text="Saldo:")
        self.value_balance = ctk.CTkLabel(self, text="")

        self.label_faults = ctk.CTkLabel(self, text="Fallas Registradas:")
        self.value_faults = ctk.CTkLabel(self, text="")

        # Colocarlos en la grilla
        self.label_bank.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.value_bank.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.label_nationality.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.value_nationality.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        self.label_number_account.grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.value_number_account.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        self.label_ci.grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.value_ci.grid(row=4, column=1, sticky="w", padx=10, pady=5)

        self.label_name.grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.value_name.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        self.label_lastname.grid(row=6, column=0, sticky="e", padx=10, pady=5)
        self.value_lastname.grid(row=6, column=1, sticky="w", padx=10, pady=5)

        self.label_phone.grid(row=7, column=0, sticky="e", padx=10, pady=5)
        self.value_phone.grid(row=7, column=1, sticky="w", padx=10, pady=5)

        self.label_address.grid(row=8, column=0, sticky="e", padx=10, pady=5)
        self.value_address.grid(row=8, column=1, sticky="w", padx=10, pady=5)

        self.label_balance.grid(row=9, column=0, sticky="e", padx=10, pady=5)
        self.value_balance.grid(row=9, column=1, sticky="w", padx=10, pady=5)

        self.label_faults.grid(row=10, column=0, sticky="e", padx=10, pady=5)
        self.value_faults.grid(row=10, column=1, sticky="w", padx=10, pady=5)


# Ejecutar interfaz
if __name__ == "__main__":
    app = EkoUI()
    app.mainloop()
