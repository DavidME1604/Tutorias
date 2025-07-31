import customtkinter as ctk
from tkinter import messagebox
from resources.dashboard import MainApp
import pyodbc
import os
import sys
from PIL import Image


# Detectar ruta correcta para PyInstaller
def obtener_ruta_relativa(ruta_archivo):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_archivo)
    return ruta_archivo


CREDENCIALES = {
    "fis": {
        "contrasena": "1234",
        "conexion": (
            "DRIVER={SQL Server};"
            "SERVER=26.33.159.111\\MSSQLSERVER_BD;"
            "DATABASE=TutoriasFIS;"
            "UID=sa;"
            "PWD=123456789"
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

        self.frame_der = ctk.CTkFrame(self, width=400, height=400,
                                      fg_color="#0f1a3c", corner_radius=0)
        self.frame_der.grid(row=0, column=1, sticky="nswe")

        self.crear_interfaz()

    # ------------------------------------------------------------
    def crear_interfaz(self):
        try:
            ruta_imagen = obtener_ruta_relativa("resources/login.png")
            imagen = Image.open(ruta_imagen)
            login_img = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(400, 400))

            ctk.CTkLabel(self.frame_izq, image=login_img, text="")\
                .place(relx=0, rely=0, relwidth=1, relheight=1)

        except Exception as e:
            print("Error cargando imagen:", e)

        ctk.CTkLabel(self.frame_der, text="¡Bienvenido!",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="white")\
            .place(relx=0.5, rely=0.15, anchor="center")

        ctk.CTkLabel(self.frame_der, text="Usuario:",
                     text_color="white", font=ctk.CTkFont(size=16))\
            .place(relx=0.2, rely=0.30, anchor="w")
        self.entry_user = ctk.CTkEntry(self.frame_der, width=250, height=35,
                                       corner_radius=20)
        self.entry_user.place(relx=0.2, rely=0.38)

        ctk.CTkLabel(self.frame_der, text="Contraseña:",
                     text_color="white", font=ctk.CTkFont(size=16))\
            .place(relx=0.2, rely=0.54, anchor="w")
        self.entry_pass = ctk.CTkEntry(self.frame_der, show="*",
                                       width=250, height=35, corner_radius=20)
        self.entry_pass.place(relx=0.2, rely=0.62)

        ctk.CTkButton(self.frame_der, text="Ingresar",
                      command=self.login, width=150, height=40,
                      corner_radius=20)\
            .place(relx=0.5, rely=0.8, anchor="center")

    # ------------------------------------------------------------
    def login(self):
        usuario = self.entry_user.get().lower()
        contrasena = self.entry_pass.get()

        cred = CREDENCIALES.get(usuario)
        if cred and contrasena == cred["contrasena"]:
            try:
                conexion = pyodbc.connect(cred["conexion"])
            except Exception as e:
                messagebox.showerror("Error de conexión", str(e))
                return

            self.withdraw()
            MainApp(usuario, conexion, self).mainloop()
        else:
            messagebox.showerror("Acceso denegado", "Credenciales incorrectas")
