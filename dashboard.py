import customtkinter as ctk
from modulos import carreras, profesores, tutores, estudiantes

class MainApp(ctk.CTk):
    def __init__(self, conexion):
        super().__init__()
        self.conexion = conexion
        self.geometry("1000x600")
        self.title("Panel Principal")
        self.config(bg="#0f1a3c")

        self.menu_frame = self.crear_menu_lateral()
        self.content_frame = self.crear_contenedor_dinamico()

    def crear_menu_lateral(self):
        frame = ctk.CTkFrame(self, width=250, fg_color="#365a9c", corner_radius=20)
        frame.pack(side="left", fill="y", padx=20, pady=20)

        label = ctk.CTkLabel(frame, text="Menú", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")
        label.pack(pady=(10, 20))

        self.selector = ctk.CTkComboBox(frame, values=["Carreras", "Profesores", "Tutores", 'Estudiantes'], command=self.mostrar_modulo)
        self.selector.set("Selecciona la tabla")
        self.selector.pack(pady=10, padx=20)

        return frame

    def crear_contenedor_dinamico(self):
        frame = ctk.CTkFrame(self, fg_color="white")
        frame.pack(side="right", expand=True, fill="both", padx=10, pady=20)
        return frame

    def mostrar_modulo(self, seleccion):
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

