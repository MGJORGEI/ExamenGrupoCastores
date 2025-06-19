import tkinter as tk
from tkinter import messagebox
import pyodbc

# Conexión a la base
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'DATABASE=noticias;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Funciones para cargar noticias
def cargar_noticias():
    cursor.execute("SELECT idnoticia, titulo FROM noticias")
    return cursor.fetchall()

def cargar_comentarios(idnoticia):
    cursor.execute("""
        SELECT c.idcomentario, u.correo, c.contenido, c.fecha_hora, c.idcomentario_respuesta
        FROM comentarios c
        JOIN usuarios u ON c.idusuario = u.idusuario
        WHERE c.idnoticia = ?
        ORDER BY c.fecha_hora
    """, (idnoticia,))
    return cursor.fetchall()

# Guardar comentario o respuesta
def guardar_comentario(idnoticia, idusuario, contenido, idcomentario_respuesta=None):
    cursor.execute("""
        INSERT INTO comentarios (idnoticia, idusuario, contenido, idcomentario_respuesta)
        VALUES (?, ?, ?, ?)
    """, (idnoticia, idusuario, contenido, idcomentario_respuesta))
    conn.commit()

# GUI
root = tk.Tk()
root.title("Noticias y Comentarios")
root.geometry("800x600")

# Lista de noticias
tk.Label(root, text="Noticias:").pack()
lst_noticias = tk.Listbox(root, width=80)
lst_noticias.pack()

for noticia in cargar_noticias():
    lst_noticias.insert(tk.END, f"{noticia.idnoticia} - {noticia.titulo}")

# Mostrar comentarios
tk.Label(root, text="Comentarios:").pack()
lst_comentarios = tk.Listbox(root, width=100, height=10)
lst_comentarios.pack()

def mostrar_comentarios(event):
    lst_comentarios.delete(0, tk.END)
    seleccion = lst_noticias.get(tk.ACTIVE)
    if seleccion:
        idnoticia = int(seleccion.split(" - ")[0])
        comentarios = cargar_comentarios(idnoticia)
        for c in comentarios:
            prefijo = "  ↳ " if c.idcomentario_respuesta else ""
            lst_comentarios.insert(tk.END, f"{prefijo}{c.correo}: {c.contenido} ({c.fecha_hora})")

lst_noticias.bind('<<ListboxSelect>>', mostrar_comentarios)

# Entradas para nuevo comentario
tk.Label(root, text="ID Usuario:").pack()
entry_usuario = tk.Entry(root, width=10)
entry_usuario.pack()

tk.Label(root, text="Comentario:").pack()
txt_comentario = tk.Text(root, width=80, height=4)
txt_comentario.pack()

btn_comentar = tk.Button(root, text="Enviar comentario", command=lambda: enviar_comentario())
btn_comentar.pack()

def enviar_comentario():
    seleccion = lst_noticias.get(tk.ACTIVE)
    if not seleccion:
        messagebox.showerror("Error", "Selecciona una noticia")
        return
    idnoticia = int(seleccion.split(" - ")[0])
    idusuario = entry_usuario.get()
    contenido = txt_comentario.get("1.0", tk.END).strip()
    if not idusuario or not contenido:
        messagebox.showerror("Error", "Completa todos los campos")
        return
    guardar_comentario(idnoticia, int(idusuario), contenido)
    messagebox.showinfo("Éxito", "Comentario guardado")
    txt_comentario.delete("1.0", tk.END)
    mostrar_comentarios(None)

root.mainloop()
