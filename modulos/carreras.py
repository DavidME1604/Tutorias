import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# ----------------------------------------------------------------------
# Ajuste global de escala (antes de crear cualquier widget)
# ----------------------------------------------------------------------
ctk.set_widget_scaling(1.0)   # tamaño de controles
ctk.set_window_scaling(1.0)   # DPI del texto

# ----------------------------------------------------------------------
# Función para construir el módulo de “Gestión de Carreras”
# ----------------------------------------------------------------------
def mostrar(parent: ctk.CTkFrame, conexion):
    # -------------   Helpers CRUD   -----------------------------------
    def cargar_datos():
        tabla.delete(*tabla.get_children())
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo_carrera, nombre, modalidad, codigo_facultad FROM v_Carrera")
        for fila in cursor.fetchall():
            tabla.insert("", "end", values=(fila.codigo_carrera,
                                            fila.nombre,
                                            fila.modalidad,
                                            fila.codigo_facultad))

    def on_seleccion(event):
        sel = tabla.selection()
        if sel:
            valores = tabla.item(sel[0], 'values')
            if valores:
                entry_codigo.delete(0, tk.END); entry_codigo.insert(0, valores[0])
                entry_nombre.delete(0, tk.END); entry_nombre.insert(0, valores[1])
                entry_modalidad.delete(0, tk.END); entry_modalidad.insert(0, valores[2])

    def insertar():
        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC spInsertarCarrera ?, ?, ?, ?",
                           (entry_codigo.get(), entry_nombre.get(),
                            entry_modalidad.get(), 'FCA'))
            conexion.commit()
            cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar():
        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC spActualizarCarrera ?, ?, ?",
                           (entry_codigo.get(), entry_nombre.get(),
                            entry_modalidad.get()))
            conexion.commit()
            cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar():
        try:
            cursor = conexion.cursor()
            cursor.execute("EXEC spEliminarCarrera ?", (entry_codigo.get(),))
            conexion.commit()
            cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar():
        entry_codigo.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_modalidad.delete(0, tk.END)
        tabla.selection_remove(tabla.selection())

    # -------------   UI   ---------------------------------------------
    parent.configure(fg_color="#2e2e2e")

    ctk.CTkLabel(parent, text="Gestión de Carreras",
                 font=ctk.CTkFont(size=22), text_color="white").pack(pady=10)

    # ---- Formulario ---------------------------------------------------
    form_frame = ctk.CTkFrame(parent, fg_color="#3a3a3a")
    form_frame.pack(pady=10)

    ctk.CTkLabel(form_frame, text="Código:", text_color="white") \
        .grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_codigo = ctk.CTkEntry(form_frame, width=200)
    entry_codigo.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(form_frame, text="Nombre:", text_color="white") \
        .grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_nombre = ctk.CTkEntry(form_frame, width=200)
    entry_nombre.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(form_frame, text="Modalidad:", text_color="white") \
        .grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_modalidad = ctk.CTkEntry(form_frame, width=200)
    entry_modalidad.grid(row=2, column=1, padx=5, pady=5)

    # ---- Tabla --------------------------------------------------------
    tabla_frame = ctk.CTkFrame(parent, fg_color="#2e2e2e")
    tabla_frame.pack(pady=10, fill="both", expand=True)

    # Estilo para Treeview (ligado al contenedor 'parent')
    style = ttk.Style(parent)
    style.theme_use("clam")
    style.configure("Carreras.Treeview",
                    background="#3a3a3a",
                    foreground="white",
                    fieldbackground="#3a3a3a",
                    font=("Arial", 13),
                    rowheight=32)          # adapta si usas otra fuente/tamaño
    style.configure("Carreras.Treeview.Heading",
                    font=("Arial", 14, "bold"),
                    background="#2e2e2e",
                    foreground="white")
    style.map("Carreras.Treeview",
              background=[('selected', '#4a90e2')])

    # Scrollbar
    tabla_scroll = tk.Scrollbar(tabla_frame, orient="vertical")
    tabla_scroll.pack(side="right", fill="y")

    # Treeview con el estilo personalizado
    tabla = ttk.Treeview(tabla_frame,
                         columns=("codigo", "nombre", "modalidad"),
                         show="headings",
                         yscrollcommand=tabla_scroll.set,
                         height=10,
                         style="Carreras.Treeview")
    tabla.heading("codigo", text="Código")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("modalidad", text="Modalidad")

    tabla.column("codigo", width=120, anchor="center")
    tabla.column("nombre", width=350, anchor="w")
    tabla.column("modalidad", width=180, anchor="center")

    tabla.pack(fill="both", expand=True)
    tabla_scroll.configure(command=tabla.yview)
    tabla.bind("<ButtonRelease-1>", on_seleccion)

    # ---- Botones ------------------------------------------------------
    btns = ctk.CTkFrame(parent, fg_color="#2e2e2e")
    btns.pack(pady=10)

    ctk.CTkButton(btns, text="Consultar", command=cargar_datos) \
        .grid(row=0, column=0, padx=5, pady=5)
    ctk.CTkButton(btns, text="Insertar",  command=insertar) \
        .grid(row=0, column=1, padx=5, pady=5)
    ctk.CTkButton(btns, text="Actualizar", command=actualizar) \
        .grid(row=0, column=2, padx=5, pady=5)
    ctk.CTkButton(btns, text="Eliminar", command=eliminar) \
        .grid(row=0, column=3, padx=5, pady=5)
    ctk.CTkButton(btns, text="Limpiar", command=limpiar) \
        .grid(row=0, column=4, padx=5, pady=5)

    # ---- Inicializa datos --------------------------------------------
    cargar_datos()
