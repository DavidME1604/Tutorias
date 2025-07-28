# ---------------------------------------------------------------
#  Módulo: Gestión de Estudiantes
#  (mismo estilo y lógica que el de Carreras)
# ---------------------------------------------------------------
import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# Asegúrate de llamar a estos dos set_* SOLO una vez en tu app principal.
ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

def mostrar(parent: ctk.CTkFrame, conexion):

    # ------------------ Helpers ---------------------------------
    def cargar_datos():
        tabla.delete(*tabla.get_children())
        with conexion.cursor() as cur:
            cur.execute("""
                SELECT  codigo_unico,
                        nombre,
                        apellido,
                        correo_institucional,
                        codigo_tutor,
                        codigo_carrera,
                        codigo_facultad
                FROM v_Estudiante
                ORDER BY apellido, nombre
            """)
            for codigo, nombre, apellido, correo, tutor, carrera, facultad in cur.fetchall():
                tabla.insert(
                    "", "end",
                    values=(codigo, nombre, apellido, correo, tutor, carrera, facultad)
                )

    def on_seleccion(event):
        sel = tabla.selection()
        if sel:
            codigo, nombre, apellido, correo, tutor, carrera, facultad = tabla.item(sel[0], "values")
            entry_codigo.delete(0, tk.END);   entry_codigo.insert(0, codigo)
            entry_nombre.delete(0, tk.END);   entry_nombre.insert(0, nombre)
            entry_apellido.delete(0, tk.END); entry_apellido.insert(0, apellido)
            entry_correo.delete(0, tk.END);   entry_correo.insert(0, correo)
            entry_tutor.delete(0, tk.END);    entry_tutor.insert(0, tutor)
            entry_carrera.delete(0, tk.END);  entry_carrera.insert(0, carrera)
            entry_facultad.delete(0, tk.END); entry_facultad.insert(0, facultad)

    def insertar():
        try:
            with conexion.cursor() as cur:
                cur.execute("EXEC spInsertarEstudiante ?,?,?,?,?,?,?",
                            (entry_codigo.get(), entry_nombre.get(), entry_apellido.get(),
                             entry_correo.get(), entry_tutor.get(),
                             entry_carrera.get(), entry_facultad.get()))
            conexion.commit(); cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))

    def actualizar():
        try:
            with conexion.cursor() as cur:
                cur.execute("EXEC spActualizarEstudiante ?,?,?,?,?,?,?",
                            (entry_codigo.get(), entry_nombre.get(), entry_apellido.get(),
                             entry_correo.get(), entry_tutor.get(),
                             entry_carrera.get(), entry_facultad.get()))
            conexion.commit(); cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar():
        try:
            with conexion.cursor() as cur:
                cur.execute("EXEC spEliminarEstudiante ?", entry_codigo.get())
            conexion.commit(); cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

    def limpiar():
        for ent in (entry_codigo, entry_nombre, entry_apellido, entry_correo,
                    entry_tutor, entry_carrera, entry_facultad):
            ent.delete(0, tk.END)
        tabla.selection_remove(tabla.selection())

    # ------------------ UI --------------------------------------
    parent.configure(fg_color="#2e2e2e")
    ctk.CTkLabel(parent, text="Gestión de Estudiantes",
                 font=ctk.CTkFont(size=22), text_color="white").pack(pady=10)

    # ---- Formulario -------------------------------------------
    form = ctk.CTkFrame(parent, fg_color="#3a3a3a"); form.pack(pady=10)

    def fila_form(r, texto):
        ctk.CTkLabel(form, text=texto, text_color="white") \
            .grid(row=r, column=0, sticky="e", padx=5, pady=5)
        e = ctk.CTkEntry(form, width=220)
        e.grid(row=r, column=1, padx=5, pady=5)
        return e

    entry_codigo   = fila_form(0, "Código Único:")
    entry_nombre   = fila_form(1, "Nombre:")
    entry_apellido = fila_form(2, "Apellido:")
    entry_correo   = fila_form(3, "Correo inst.:")
    entry_tutor    = fila_form(4, "Código Tutor:")
    entry_carrera  = fila_form(5, "Código Carrera:")
    entry_facultad = fila_form(6, "Código Facultad:")

    # ---- Botones (ahora antes de la tabla) --------------------
    btns = ctk.CTkFrame(parent, fg_color="#2e2e2e")
    btns.pack(pady=(5, 0))
    for i, (txt, cmd) in enumerate([
        ("Consultar", cargar_datos),
        ("Insertar",  insertar),
        ("Actualizar", actualizar),
        ("Eliminar",  eliminar),
        ("Limpiar",   limpiar)
    ]):
        ctk.CTkButton(btns, text=txt, command=cmd) \
            .grid(row=0, column=i, padx=4, pady=4)

    # ---- Tabla ------------------------------------------------
    tabla_frame = ctk.CTkFrame(parent, fg_color="#2e2e2e")
    tabla_frame.pack(pady=10, fill="both", expand=True)

    estilo = ttk.Style(parent)
    estilo.theme_use("clam")
    estilo.configure("Estudiantes.Treeview",
                     background="#3a3a3a",
                     foreground="white",
                     fieldbackground="#3a3a3a",
                     font=("Arial", 13),
                     rowheight=32)
    estilo.configure("Estudiantes.Treeview.Heading",
                     font=("Arial", 14, "bold"),
                     background="#2e2e2e",
                     foreground="white")
    estilo.map("Estudiantes.Treeview",
               background=[('selected', '#4a90e2')])

    scroll = tk.Scrollbar(tabla_frame, orient="vertical")
    scroll.pack(side="right", fill="y")

    cols = ("codigo", "nombre", "apellido", "correo",
            "tutor", "carrera", "facultad")
    tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings",
                         yscrollcommand=scroll.set, height=10,
                         style="Estudiantes.Treeview")

    for col, ancho, anchor in [
        ("codigo",   110, "center"),
        ("nombre",   120, "w"),
        ("apellido", 120, "w"),
        ("correo",   220, "w"),
        ("tutor",    110, "center"),
        ("carrera",  110, "center"),
        ("facultad", 110, "center")]:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=ancho, anchor=anchor)

    tabla.pack(fill="both", expand=True)
    scroll.configure(command=tabla.yview)
    tabla.bind("<ButtonRelease-1>", on_seleccion)

    # ---- Inicializar datos -----------------------------------
    cargar_datos()
