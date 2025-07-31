import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

def mostrar(parent: ctk.CTkFrame, conexion, nodo_actual):

    # ------------------  Helpers  -------------------------------------
    def cargar_datos():
        tabla.delete(*tabla.get_children())
        with conexion.cursor() as cur:
            if nodo_actual == "fis":
                cur.execute("""
                    SELECT codigo_carrera, nombre, modalidad, codigo_facultad
                    FROM v_Carrera WHERE codigo_facultad = 'FIS'
                """)
            else:
                cur.execute("""
                    SELECT codigo_carrera, nombre, modalidad, codigo_facultad
                    FROM v_Carrera
                """)
            for codigo, nombre, modalidad, facultad in cur.fetchall():   # <<<
                tabla.insert("", "end", values=(codigo, nombre,
                                                modalidad, facultad))

    def on_seleccion(event):
        sel = tabla.selection()
        if sel:
            codigo, nombre, modalidad, facultad = tabla.item(sel[0], "values")
            entry_codigo.delete(0, tk.END);     entry_codigo.insert(0, codigo)
            entry_nombre.delete(0, tk.END);     entry_nombre.insert(0, nombre)
            entry_modalidad.delete(0, tk.END);  entry_modalidad.insert(0, modalidad)
            entry_facultad.delete(0, tk.END);   entry_facultad.insert(0, facultad)

    def insertar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis":
                    if not entry_facultad.get() == "FIS":
                        messagebox.showerror("Error", "La facultad debe ser FIS")
                        return
                    else:
                        cur.execute("EXEC spInsertarCarrera ?, ?, ?, ?",
                                    (entry_codigo.get(), entry_nombre.get(),
                                    entry_modalidad.get(), entry_facultad.get()))
                else:
                    cur.execute("EXEC spInsertarCarrera ?, ?, ?, ?",
                                    (entry_codigo.get(), entry_nombre.get(),
                                    entry_modalidad.get(), entry_facultad.get()))
            conexion.commit(); cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al insertar", str(e))

    def actualizar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis":
                    if not entry_facultad.get() == "FIS":
                        messagebox.showerror("Error", "La facultad debe ser FIS")
                        return
                    else:
                        cur.execute("EXEC spActualizarCarrera ?, ?, ?",
                                    (entry_codigo.get(), entry_nombre.get(),
                                     entry_modalidad.get()))
                else:
                    cur.execute("EXEC spActualizarCarrera ?, ?, ?, ?",
                                    (entry_codigo.get(), entry_nombre.get(),
                                     entry_modalidad.get(), entry_facultad.get()))
            conexion.commit(); cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis":
                    if not entry_facultad.get() == "FIS":
                        messagebox.showerror("Error", "La facultad debe ser FIS")
                        return
                    else:
                        cur.execute("EXEC spEliminarCarrera ?, ?", (entry_codigo.get(), entry_facultad.get()))
                else:
                    cur.execute("EXEC spEliminarCarrera ?, ?", (entry_codigo.get(), entry_facultad.get()))
            conexion.commit(); cargar_datos()
        except Exception as e:
            messagebox.showerror("Error al eliminar", str(e))

    def limpiar():
        for ent in (entry_codigo, entry_nombre, entry_modalidad, entry_facultad):
            ent.delete(0, tk.END)
        tabla.selection_remove(tabla.selection())

    def consultar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis":
                    if entry_facultad.get().strip().upper() != "FIS":
                        messagebox.showerror("Error", "La facultad debe ser FIS")
                        return

                tabla.delete(*tabla.get_children())

                codigo    = entry_codigo.get().strip() or None
                nombre    = entry_nombre.get().strip() or None
                modalidad = entry_modalidad.get().strip() or None
                facultad  = entry_facultad.get().strip() or None


                cur.execute("""
                    EXEC spBuscarCarreraDinamico ?, ?, ?, ?
                """, (codigo, nombre, modalidad, facultad))
                for codigo, nombre, modalidad, facultad in cur.fetchall():
                    tabla.insert("", "end", values=(codigo, nombre, modalidad, facultad))

        except Exception as e:
            messagebox.showerror("Error al consultar", str(e))


            
    # ------------------  UI  ------------------------------------------
    parent.configure(fg_color="#2e2e2e")
    ctk.CTkLabel(parent, text="Gestión de Carreras",
                 font=ctk.CTkFont(size=22), text_color="white").pack(pady=10)

    form = ctk.CTkFrame(parent, fg_color="#3a3a3a"); form.pack(pady=10)

    def fila_form(r, texto):
        ctk.CTkLabel(form, text=texto, text_color="white") \
            .grid(row=r, column=0, sticky="e", padx=5, pady=5)
        e = ctk.CTkEntry(form, width=200); e.grid(row=r, column=1, padx=5, pady=5)
        return e

    entry_codigo    = fila_form(0, "Código:")
    entry_nombre    = fila_form(1, "Nombre:")
    entry_modalidad = fila_form(2, "Modalidad:")
    entry_facultad  = fila_form(3, "Código Facultad:")

    # ---- Tabla --------------------------------------------------------
    tabla_frame = ctk.CTkFrame(parent, fg_color="#2e2e2e")
    tabla_frame.pack(pady=10, fill="both", expand=True)

    estilo = ttk.Style(parent)
    estilo.theme_use("clam")
    estilo.configure("Carreras.Treeview", background="#3a3a3a",
                     foreground="white", fieldbackground="#3a3a3a",
                     font=("Arial", 13), rowheight=32)
    estilo.configure("Carreras.Treeview.Heading",
                     font=("Arial", 14, "bold"),
                     background="#2e2e2e", foreground="white")
    estilo.map("Carreras.Treeview",
               background=[('selected', '#4a90e2')])

    scroll = tk.Scrollbar(tabla_frame, orient="vertical"); scroll.pack(side="right", fill="y")

    cols = ("codigo", "nombre", "modalidad", "facultad")
    tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings",
                         yscrollcommand=scroll.set, height=10,
                         style="Carreras.Treeview")
    for col, ancho, anchor in [
        ("codigo", 110, "center"),
        ("nombre", 280, "w"),
        ("modalidad", 140, "center"),
        ("facultad", 120, "center")]:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=ancho, anchor=anchor)

    tabla.pack(fill="both", expand=True)
    scroll.configure(command=tabla.yview)
    tabla.bind("<ButtonRelease-1>", on_seleccion)

    # ---- Botones ------------------------------------------------------
    btns = ctk.CTkFrame(parent, fg_color="#2e2e2e"); btns.pack(pady=10)
    for i, (txt, cmd) in enumerate([
        ("Consultar", consultar),
        ("Insertar",  insertar),
        ("Actualizar", actualizar),
        ("Eliminar",  eliminar),
        ("Limpiar",   limpiar)]):
        ctk.CTkButton(btns, text=txt, command=cmd) \
            .grid(row=0, column=i, padx=5, pady=5)

    cargar_datos()
