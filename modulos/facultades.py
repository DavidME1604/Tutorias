# ---------------------------------------------------------------
#  Módulo: Gestión de Facultades
#  (mismo estilo y lógica que el de Estudiantes/Carreras)
# ---------------------------------------------------------------
import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# Asegúrate de llamar a estos dos set_* SOLO una vez en tu app principal.
ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

def mostrar(parent: ctk.CTkFrame, conexion, nodo_actual):
    # ------------------ Helpers ---------------------------------
    def cargar_datos():
        tabla.delete(*tabla.get_children())
        with conexion.cursor() as cur:
            cur.execute("""
                    SELECT codigo_facultad, nombre
                    FROM Facultad
                    ORDER BY codigo_facultad
                """)
            for codigo, nombre in cur.fetchall():
                tabla.insert("", "end", values=(codigo, nombre))

    def on_seleccion(_event):
        sel = tabla.selection()
        if sel:
            codigo, nombre = tabla.item(sel[0], "values")
            entry_codigo.delete(0, tk.END); entry_codigo.insert(0, codigo)
            entry_nombre.delete(0, tk.END); entry_nombre.insert(0, nombre)

    def insertar():
        try:
            with conexion.cursor() as cur:
                cur.execute("EXEC spInsertarFacultad ?, ?",
                            (entry_codigo.get(), entry_nombre.get()))
            conexion.commit(); cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))

    def actualizar():
        try:
            with conexion.cursor() as cur:
                cur.execute("EXEC spActualizarFacultad ?, ?",
                            (entry_codigo.get(), entry_nombre.get()))
            conexion.commit(); cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar():
        try:
            with conexion.cursor() as cur:
                cur.execute("EXEC spEliminarFacultad ?", entry_codigo.get())
            conexion.commit(); cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

    def limpiar():
        for ent in (entry_codigo, entry_nombre):
            ent.delete(0, tk.END)
        tabla.selection_remove(tabla.selection())

    # ------------------ UI --------------------------------------
    parent.configure(fg_color="#2e2e2e")
    ctk.CTkLabel(parent, text="Gestión de Facultades",
                 font=ctk.CTkFont(size=22), text_color="white").pack(pady=10)

    # ---- Formulario -------------------------------------------
    form = ctk.CTkFrame(parent, fg_color="#3a3a3a"); form.pack(pady=10)

    def fila_form(r, texto):
        ctk.CTkLabel(form, text=texto, text_color="white").grid(
            row=r, column=0, sticky="e", padx=5, pady=5)
        e = ctk.CTkEntry(form, width=220)
        e.grid(row=r, column=1, padx=5, pady=5)
        return e

    entry_codigo = fila_form(0, "Código Facultad:")
    entry_nombre = fila_form(1, "Nombre:")

    # ---- Botones ----------------------------------------------
    btns = ctk.CTkFrame(parent, fg_color="#2e2e2e")
    btns.pack(pady=(5, 0))
    for i, (txt, cmd) in enumerate([
        ("Consultar", cargar_datos),
        ("Insertar",  insertar),
        ("Actualizar", actualizar),
        ("Eliminar",  eliminar),
        ("Limpiar",   limpiar)
    ]):
        ctk.CTkButton(btns, text=txt, command=cmd)\
            .grid(row=0, column=i, padx=4, pady=4)

    # ---- Tabla -------------------------------------------------
    tabla_frame = ctk.CTkFrame(parent, fg_color="#2e2e2e")
    tabla_frame.pack(pady=10, fill="both", expand=True)

    estilo = ttk.Style(parent)
    estilo.theme_use("clam")
    estilo.configure("Facultades.Treeview",
                     background="#3a3a3a", foreground="white",
                     fieldbackground="#3a3a3a", font=("Arial", 13),
                     rowheight=32)
    estilo.configure("Facultades.Treeview.Heading",
                     font=("Arial", 14, "bold"),
                     background="#2e2e2e", foreground="white")
    estilo.map("Facultades.Treeview",
               background=[('selected', '#4a90e2')])

    scroll = tk.Scrollbar(tabla_frame, orient="vertical")
    scroll.pack(side="right", fill="y")

    cols = ("codigo", "nombre")
    tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings",
                         yscrollcommand=scroll.set, height=10,
                         style="Facultades.Treeview")
    tabla.heading("codigo", text="Código")
    tabla.column("codigo", width=120, anchor="center")
    tabla.heading("nombre", text="Nombre")
    tabla.column("nombre", width=260, anchor="w")

    tabla.pack(fill="both", expand=True)
    scroll.configure(command=tabla.yview)
    tabla.bind("<ButtonRelease-1>", on_seleccion)

    # ---- Inicializar datos ------------------------------------
    cargar_datos()
