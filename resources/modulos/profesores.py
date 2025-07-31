# ---------------------------------------------------------------
#  Módulo: Gestión de Profesores
# ---------------------------------------------------------------
import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

def mostrar(parent: ctk.CTkFrame, conexion, nodo_actual):

    # ------------------ Helpers ---------------------------------
    def cargar_datos():
        tabla.delete(*tabla.get_children())
        with conexion.cursor() as cur:
            if nodo_actual == "fis" :
                cur.execute("""
                    SELECT  codigo_profesor,
                            nombre,
                            apellido,
                            titulo,               
                            correo,
                            codigo_facultad
                    FROM v_Profesor
                    WHERE codigo_facultad = 'FIS'
                    ORDER BY apellido, nombre
                """)
            else:
                cur.execute("""
                    SELECT  codigo_profesor,
                            nombre,
                            apellido,
                            titulo,              
                            correo,
                            codigo_facultad
                    FROM v_Profesor
                    ORDER BY apellido, nombre
                """)
            for cod, nom, ape, tit, mail, fac in cur.fetchall():
                tabla.insert("", "end",
                             values=(cod, nom, ape, tit, mail, fac))

    def on_sel(_):
        if not tabla.selection():
            return
        cod, nom, ape, tit, mail, fac = tabla.item(
            tabla.selection()[0], "values")
        e_cod.delete(0, tk.END); e_cod.insert(0, cod)
        e_nom.delete(0, tk.END); e_nom.insert(0, nom)
        e_ape.delete(0, tk.END); e_ape.insert(0, ape)
        e_tit.delete(0, tk.END); e_tit.insert(0, tit)
        e_mail.delete(0, tk.END); e_mail.insert(0, mail)
        e_fac.delete(0, tk.END); e_fac.insert(0, fac)

    def insertar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis" and not e_fac.get() == "FIS":
                    messagebox.showerror("Error", "El profesor debe ser de la facultad FIS")
                    return
                else:
                    cur.execute("EXEC spInsertarProfesorInfo ?,?,?,?,?,?",
                                (e_cod.get(), e_nom.get(), e_ape.get(),
                                e_tit.get(), e_mail.get(), e_fac.get()))
            conexion.commit(); cargar_datos()
        except Exception as err:
            messagebox.showerror("Error al insertar", str(err))

    def actualizar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis" and not e_fac.get() == "FIS":
                    messagebox.showerror("Error", "El profesor debe ser de la facultad FIS")
                    return
                else:
                    cur.execute("EXEC spActualizarProfesorInfo ?,?,?,?,?,?",
                                (e_cod.get(), e_nom.get(), e_ape.get(),
                                e_tit.get(), e_mail.get(), e_fac.get()))
            conexion.commit(); cargar_datos()
        except Exception as err:
            messagebox.showerror("Error al actualizar", str(err))

    def eliminar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis" and not e_fac.get() == "FIS":
                    messagebox.showerror("Error", "El profesor debe ser de la facultad FIS")
                    return
                else:
                    cur.execute("EXEC spEliminarProfesorInfo ?, ?",( e_cod.get(), e_fac.get()))
            conexion.commit(); cargar_datos()
        except Exception as err:
            messagebox.showerror("Error al eliminar", str(err))

    def limpiar():
        for ent in (e_cod, e_nom, e_ape, e_tit, e_mail, e_fac):
            ent.delete(0, tk.END)
        tabla.selection_remove(tabla.selection())

    def consultar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis" and e_fac.get().strip().upper() != "FIS":
                    messagebox.showerror("Error", "La facultad debe ser FIS")
                    return

                tabla.delete(*tabla.get_children())

                # Obtener valores de los campos
                cod = e_cod.get().strip() or None
                nom = e_nom.get().strip() or None
                ape = e_ape.get().strip() or None
                tit = e_tit.get().strip() or None
                mail = e_mail.get().strip() or None
                fac = e_fac.get().strip() or None

                cur.execute("""
                    EXEC spBuscarProfesorDinamico ?, ?, ?, ?, ?, ?
                """, (cod, nom, ape, tit, mail, fac))

                resultados = cur.fetchall()
                if not resultados:
                    messagebox.showinfo("Consulta vacía", "No se encontraron registros.")
                else:
                    for cod, nom, ape, tit, mail, fac in resultados:
                        tabla.insert("", "end", values=(cod, nom, ape, tit, mail, fac))

        except Exception as err:
            messagebox.showerror("Error al consultar", str(err))


    # ------------------ UI --------------------------------------
    parent.configure(fg_color="#2e2e2e")
    ctk.CTkLabel(parent, text="Gestión de Profesores",
                 font=ctk.CTkFont(size=22), text_color="white").pack(pady=10)

    form = ctk.CTkFrame(parent, fg_color="#3a3a3a"); form.pack(pady=10)

    def fila(r, txt):
        ctk.CTkLabel(form, text=txt, text_color="white") \
            .grid(row=r, column=0, sticky="e", padx=5, pady=5)
        ent = ctk.CTkEntry(form, width=220); ent.grid(row=r, column=1, padx=5, pady=5)
        return ent

    e_cod = fila(0, "Código:")
    e_nom = fila(1, "Nombre:")
    e_ape = fila(2, "Apellido:")
    e_tit = fila(3, "Título:")
    e_mail= fila(4, "Correo:")
    e_fac = fila(5, "Facultad:")

    # Botones encima de la tabla
    btns = ctk.CTkFrame(parent, fg_color="#2e2e2e"); btns.pack(pady=(5, 0))
    for i, (txt, cmd) in enumerate([
        ("Consultar", consultar), ("Insertar", insertar),
        ("Actualizar", actualizar), ("Eliminar", eliminar),
        ("Limpiar", limpiar)
    ]):
        ctk.CTkButton(btns, text=txt, command=cmd) \
            .grid(row=0, column=i, padx=4, pady=4)

    # Tabla
    frame_tabla = ctk.CTkFrame(parent, fg_color="#2e2e2e")
    frame_tabla.pack(pady=10, fill="both", expand=True)

    sty = ttk.Style(parent); sty.theme_use("clam")
    sty.configure("Prof.Treeview", background="#3a3a3a", foreground="white",
                  fieldbackground="#3a3a3a", font=("Arial", 13), rowheight=32)
    sty.configure("Prof.Treeview.Heading",
                  font=("Arial", 14, "bold"),
                  background="#2e2e2e", foreground="white")

    cols = ("codigo", "nombre", "apellido", "titulo", "correo", "facultad")
    tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                         style="Prof.Treeview", height=10)
    for col, w, a in [
        ("codigo",110,"center"), ("nombre",120,"w"), ("apellido",120,"w"),
        ("titulo",140,"center"), ("correo",220,"w"), ("facultad",110,"center")]:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=w, anchor=a)

    tabla.pack(fill="both", expand=True)
    ttk.Scrollbar(frame_tabla, command=tabla.yview)\
        .pack(side="right", fill="y")
    tabla.bind("<ButtonRelease-1>", on_sel)

    cargar_datos()