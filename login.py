import customtkinter as ctk
from tkinter import messagebox
from dashboard import MainApp
import pyodbc

CREDENCIALES = {
    "fis": {
        "contrasena": "1234",
        "conexion": (
            "DRIVER={SQL Server};"
            "SERVER=26.78.150.240\SQLEXPRESS;"
            "DATABASE=TutoriasFIS;"
            "UID=sa;"
            "PWD=12"
        )
    },
    "fca": {
        "contrasena": "abcd",
        "conexion": (
            "DRIVER={SQL Server};"
            "SERVER=26.110.38.159;"
            "DATABASE=TutoriasFCA;"
            "UID=sa;"
            "PWD=P@ssw0rd"
        )
    }
}

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        self.title("Inicio de Sesión")
        self.resizable(False, False)
        self.config(bg="#0f1a3c")

        self.frame_izq = ctk.CTkFrame(self, width=400, height=400, corner_radius=0)
        self.frame_izq.grid(row=0, column=0, sticky="nswe")

        self.frame_der = ctk.CTkFrame(self, width=400, height=400, fg_color="#0f1a3c", corner_radius=0)
        self.frame_der.grid(row=0, column=1, sticky="nswe")

        self.crear_interfaz()

    def crear_interfaz(self):
        try:
            from PIL import Image
            imagen = ctk.CTkImage(light_image=Image.open("Img/login.png"), size=(400, 400))
            label_imagen = ctk.CTkLabel(self.frame_izq, image=imagen, text="")
            label_imagen.place(relx=0, rely=0, relwidth=1, relheight=1)
        except:
            ctk.CTkLabel(self.frame_izq, text="(imagen no encontrada)").pack(expand=True)

        ctk.CTkLabel(self.frame_der, text="¡Bienvenido!", font=ctk.CTkFont(size=24, weight="bold"), text_color="white").place(relx=0.5, rely=0.15, anchor="center")

        ctk.CTkLabel(self.frame_der, text="Usuario:", text_color="white", font=ctk.CTkFont(size=16)).place(relx=0.2, rely=0.30, anchor="w")
        self.entry_user = ctk.CTkEntry(self.frame_der, width=250, height=35, corner_radius=20)
        self.entry_user.place(relx=0.2, rely=0.38)

        ctk.CTkLabel(self.frame_der, text="Contraseña:", text_color="white", font=ctk.CTkFont(size=16)).place(relx=0.2, rely=0.54, anchor="w")
        self.entry_pass = ctk.CTkEntry(self.frame_der, show="*", width=250, height=35, corner_radius=20)
        self.entry_pass.place(relx=0.2, rely=0.62)

        ctk.CTkButton(self.frame_der, text="Ingresar", command=self.login, width=150, height=40, corner_radius=20).place(relx=0.5, rely=0.8, anchor="center")

    def login(self):
        usuario = self.entry_user.get().lower()
        contrasena = self.entry_pass.get()

        if usuario in CREDENCIALES and contrasena == CREDENCIALES[usuario]["contrasena"]:
            try:
                conexion = pyodbc.connect(CREDENCIALES[usuario]["conexion"])
                self.withdraw()
                MainApp(conexion).mainloop()
            except Exception as e:
                messagebox.showerror("Error de conexión", str(e))
        else:
            messagebox.showerror("Acceso denegado", "Credenciales incorrectas")

