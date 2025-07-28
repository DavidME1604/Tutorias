import customtkinter as ctk
from modulos import carreras, profesores, tutores, estudiantes

class MainApp(ctk.CTk):
    def __init__(self, conexion, login_win):
        super().__init__()
        self.conexion   = conexion     # pyodbc connection
        self.login_win  = login_win    # referencia a la ventana de login

        # ---------- ventana principal ----------
        self.geometry("1000x600")
        self.title("Panel Principal")
        self.config(bg="#0f1a3c")

        # ---------- UI ----------
        self.menu_frame    = self.crear_menu_lateral()
        self.content_frame = self.crear_contenedor_dinamico()

    # ==================================================================
    #  Construcción de la UI
    # ==================================================================
    def crear_menu_lateral(self):
        frame = ctk.CTkFrame(self, width=250, fg_color="#365a9c", corner_radius=20)
        frame.pack(side="left", fill="y", padx=20, pady=20)

        ctk.CTkLabel(
            frame, text="Menú",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=(10, 20))

        self.selector = ctk.CTkComboBox(
            frame,
            values=["Carreras", "Profesores", "Tutores", "Estudiantes"],
            command=self.mostrar_modulo
        )
        self.selector.set("Selecciona la tabla")
        self.selector.pack(pady=10, padx=20)

        # -------- Botón Salir -----------------
        ctk.CTkButton(
            frame,
            text="Salir",
            fg_color="#c0392b",
            hover_color="#e74c3c",
            text_color="white",
            command=self.salir
        ).pack(pady=(30, 10), padx=20, fill="x")

        return frame

    def crear_contenedor_dinamico(self):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(side="right", expand=True, fill="both", padx=10, pady=20)
        return frame

    # ==================================================================
    #  Navegación entre módulos
    # ==================================================================
    def mostrar_modulo(self, seleccion: str):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if seleccion == "Carreras":
            carreras.mostrar(self.content_frame, self.conexion)
        elif seleccion == "Profesores":
            profesores.mostrar(self.content_frame, self.conexion)
        elif seleccion == "Tutores":
            tutores.mostrar(self.content_frame, self.conexion)
        elif seleccion == "Estudiantes":
            estudiantes.mostrar(self.content_frame, self.conexion)

    # ==================================================================
    #  Salir: cerrar conexión + volver al login
    # ==================================================================
    def salir(self):
        # 1. Cerrar la conexión, si sigue abierta
        try:
            if self.conexion and not self.conexion.closed:
                self.conexion.close()
        except Exception:
            pass  # ya cerrada / None

        # 2. Mostrar la ventana de login nuevamente
        if self.login_win is not None:
            self.login_win.deiconify()

        # 3. Destruir esta ventana
        self.destroy()
