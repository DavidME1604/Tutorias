# ---------------------------------------------------------------
#  Módulo: Gestión de Tutores
# ---------------------------------------------------------------

import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation

def mostrar(parent: ctk.CTkFrame, conexion, nodo_actual):

    # -------------- Helpers ------------------------------------
    def cargar_datos():
        tabla.delete(*tabla.get_children())
        with conexion.cursor() as cur:
            if nodo_actual == "fis":
                cur.execute("""
                    SELECT  codigo_profesor,
                            modalidad_tutorias,
                            estado,
                            calificacion_promedio,
                            codigo_facultad
                    FROM v_Tutor
                    WHERE codigo_facultad = 'FIS'
                    ORDER BY codigo_profesor
                """)
            else:
                cur.execute("""
                    SELECT  codigo_profesor,
                            modalidad_tutorias,
                            estado,
                            calificacion_promedio,
                            codigo_facultad
                    FROM v_Tutor
                    ORDER BY codigo_profesor
                """)
            for cod, mod, est, prom, fac in cur.fetchall():
                tabla.insert("", "end",
                             values=(cod, mod, est, prom, fac))

    def on_sel(_):
        if not tabla.selection():
            return
        cod, mod, est, prom, fac = tabla.item(
            tabla.selection()[0], "values")
        e_cod.delete(0, tk.END);  e_cod.insert(0, cod)
        e_mod.delete(0, tk.END);  e_mod.insert(0, mod)
        e_est.delete(0, tk.END);  e_est.insert(0, est)
        e_pr.delete(0, tk.END);   e_pr.insert(0, prom)
        e_fac.delete(0, tk.END);  e_fac.insert(0, fac)

    def insertar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis" and not e_fac.get() == "FIS":
                    messagebox.showerror("Error", "La facultad debe ser FIS")
                    return
                else:
                    try:
                        nota = Decimal(e_pr.get().strip())
                    except InvalidOperation:
                        messagebox.showerror("Error", "Calificación promedio inválida")
                        return
                    cur.execute("EXEC spInsertarTutor ?,?,?,?,?",
                                (e_cod.get(), e_mod.get(), e_est.get(),
                                 e_fac.get(), nota))
            conexion.commit(); cargar_datos()
        except Exception as err:
            messagebox.showerror("Error al insertar", str(err))

    def actualizar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis" and not e_fac.get() == "FIS":
                    messagebox.showerror("Error", "La facultad debe ser FIS")
                    return
                else:
                    try:
                        nota = Decimal(e_pr.get().strip())
                    except InvalidOperation:
                        messagebox.showerror("Error", "Calificación promedio inválida")
                        return
                    cur.execute("EXEC spActualizarTutor ?,?,?,?,?",
                                (e_cod.get(), e_mod.get(), e_est.get(),
                                 nota,  e_fac.get()))
            conexion.commit(); cargar_datos()
        except Exception as err:
            messagebox.showerror("Error al actualizar", str(err))

    def eliminar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis" and not e_fac.get() == "FIS":
                    messagebox.showerror("Error", "La facultad debe ser FIS")
                    return
                else:
                    cur.execute("EXEC spEliminarTutor ?, ?", (e_cod.get(), e_fac.get()))
            conexion.commit(); cargar_datos()
        except Exception as err:
            messagebox.showerror("Error al eliminar", str(err))

    def limpiar():
        for ent in (e_cod, e_mod, e_est, e_pr, e_fac):
            ent.delete(0, tk.END)
        tabla.selection_remove(tabla.selection())

    def consultar():
        try:
            with conexion.cursor() as cur:
                if nodo_actual == "fis" and e_fac.get().strip().upper() != "FIS":
                    messagebox.showerror("Error", "La facultad debe ser FIS")
                    return

                tabla.delete(*tabla.get_children())

                # Obtener valores
                cod = e_cod.get().strip() or None
                mod = e_mod.get().strip() or None
                est = e_est.get().strip() or None
                fac = e_fac.get().strip() or None

                # Intentar convertir calificación a Decimal si es válida
                try:
                    prom = Decimal(e_pr.get().strip()) if e_pr.get().strip() else None
                except InvalidOperation:
                    messagebox.showerror("Error", "Calificación promedio inválida")
                    return

                # Ejecutar procedimiento
                cur.execute("""
                    EXEC spBuscarTutorDinamico ?, ?, ?, ?, ?
                """, (cod, mod, est, prom, fac))

                resultados = cur.fetchall()
                if not resultados:
                    messagebox.showinfo("Consulta vacía", "No se encontraron registros.")
                else:
                    for cod, mod, est, prom, fac in resultados:
                        tabla.insert("", "end", values=(cod, mod, est, prom, fac))

        except Exception as err:
            messagebox.showerror("Error al consultar", str(err))


    # ------------------ UI --------------------------------------
    parent.configure(fg_color="#2e2e2e")
    ctk.CTkLabel(parent, text="Gestión de Tutores",
                 font=ctk.CTkFont(size=22), text_color="white").pack(pady=10)

    form = ctk.CTkFrame(parent, fg_color="#3a3a3a"); form.pack(pady=10)
    def fila(r, lbl):
        ctk.CTkLabel(form, text=lbl, text_color="white") \
            .grid(row=r, column=0, sticky="e", padx=5, pady=5)
        ent = ctk.CTkEntry(form, width=220); ent.grid(row=r, column=1, padx=5, pady=5)
        return ent

    e_cod = fila(0, "Código Prof.:")
    e_mod = fila(1, "Modalidad:")
    e_est = fila(2, "Estado:")
    e_pr  = fila(3, "Calif. Prom.:")
    e_fac = fila(4, "Facultad:")

    # Botones
    btns = ctk.CTkFrame(parent, fg_color="#2e2e2e"); btns.pack(pady=(5, 0))
    for i, (txt, cmd) in enumerate([
        ("Consultar", consultar), ("Insertar", insertar),
        ("Actualizar", actualizar), ("Eliminar", eliminar),
        ("Limpiar", limpiar)
    ]):
        ctk.CTkButton(btns, text=txt, command=cmd)\
            .grid(row=0, column=i, padx=4, pady=4)

    # Tabla
    frame_tabla = ctk.CTkFrame(parent, fg_color="#2e2e2e")
    frame_tabla.pack(pady=10, fill="both", expand=True)

    sty = ttk.Style(parent); sty.theme_use("clam")
    sty.configure("Tutor.Treeview", background="#3a3a3a", foreground="white",
                  fieldbackground="#3a3a3a", font=("Arial", 13), rowheight=32)
    sty.configure("Tutor.Treeview.Heading",
                  font=("Arial", 14, "bold"),
                  background="#2e2e2e", foreground="white")

    cols = ("codigo", "modalidad", "estado", "promedio", "facultad")
    tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings",
                         style="Tutor.Treeview", height=10)
    for col, w, a in [
        ("codigo",110,"center"), ("modalidad",130,"center"),
        ("estado",100,"center"), ("promedio",110,"center"),
        ("facultad",110,"center")]:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=w, anchor=a)

    tabla.pack(fill="both", expand=True)
    ttk.Scrollbar(frame_tabla, command=tabla.yview)\
        .pack(side="right", fill="y")
    tabla.bind("<ButtonRelease-1>", on_sel)

    cargar_datos()