import pyodbc
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=SISTEMAS\\MSSQLSERVER01;'
        'DATABASE=noticias;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print("Error conectando a la BD:", e)
    exit(1)

def cargar_noticias():
    cursor.execute("SELECT idnoticia, titulo FROM noticias ORDER BY fechapublicacion DESC")
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

def guardar_comentario(idnoticia, idusuario, contenido, idcomentario_respuesta=None):
    cursor.execute("""
        INSERT INTO comentarios (idnoticia, idusuario, contenido, fecha_hora, idcomentario_respuesta)
        VALUES (?, ?, ?, GETDATE(), ?)
    """, (idnoticia, idusuario, contenido, idcomentario_respuesta))
    conn.commit()

def guardar_noticia(titulo, contenido, idpersonal):
    cursor.execute("""
        INSERT INTO noticias (titulo, contenido, idpersonal, fechapublicacion)
        VALUES (?, ?, ?, GETDATE())
    """, (titulo, contenido, idpersonal))
    conn.commit()

root = tk.Tk()
root.title("Sistema de Noticias")
root.geometry("900x700")

lbl_noticias = tk.Label(root, text="Noticias:")
lbl_noticias.pack(anchor='w', padx=10)

lst_noticias = tk.Listbox(root, width=100, height=8)
lst_noticias.pack(padx=10)

lbl_contenido = tk.Label(root, text="Contenido de la noticia:")
lbl_contenido.pack(anchor='w', padx=10)

txt_contenido = scrolledtext.ScrolledText(root, width=100, height=8, state='disabled')
txt_contenido.pack(padx=10, pady=5)

lbl_comentarios = tk.Label(root, text="Comentarios:")
lbl_comentarios.pack(anchor='w', padx=10)

lst_comentarios = tk.Listbox(root, width=100, height=12)
lst_comentarios.pack(padx=10)

def actualizar_noticias():
    lst_noticias.delete(0, tk.END)
    noticias = cargar_noticias()
    for noticia in noticias:
        lst_noticias.insert(tk.END, f"{noticia.idnoticia} - {noticia.titulo}")

def mostrar_noticia(event):
    seleccion = lst_noticias.get(tk.ACTIVE)
    if not seleccion:
        return
    idnoticia = int(seleccion.split(" - ")[0])
    cursor.execute("SELECT contenido FROM noticias WHERE idnoticia = ?", (idnoticia,))
    contenido = cursor.fetchone()
    txt_contenido.config(state='normal')
    txt_contenido.delete('1.0', tk.END)
    txt_contenido.insert(tk.END, contenido[0] if contenido else "")
    txt_contenido.config(state='disabled')
    mostrar_comentarios(idnoticia)

def mostrar_comentarios(idnoticia):
    lst_comentarios.delete(0, tk.END)
    comentarios = cargar_comentarios(idnoticia)
    for c in comentarios:
        prefijo = "  ↳ " if c.idcomentario_respuesta else ""
        texto = f"{prefijo}{c.correo}: {c.contenido} ({c.fecha_hora.strftime('%Y-%m-%d %H:%M')})"
        lst_comentarios.insert(tk.END, texto)

def agregar_noticia():
    idpersonal = simpledialog.askinteger("ID Personal", "Introduce tu ID personal (interno):")
    if not idpersonal:
        messagebox.showerror("Error", "ID personal inválido")
        return
    titulo = simpledialog.askstring("Título", "Introduce el título de la noticia:")
    if not titulo:
        messagebox.showerror("Error", "El título no puede estar vacío")
        return
    contenido = simpledialog.askstring("Contenido", "Introduce el contenido de la noticia:")
    if not contenido:
        messagebox.showerror("Error", "El contenido no puede estar vacío")
        return
    guardar_noticia(titulo, contenido, idpersonal)
    messagebox.showinfo("Éxito", "Noticia agregada correctamente")
    actualizar_noticias()

def agregar_comentario():
    seleccion = lst_noticias.get(tk.ACTIVE)
    if not seleccion:
        messagebox.showerror("Error", "Selecciona una noticia primero")
        return
    idnoticia = int(seleccion.split(" - ")[0])

    idusuario = simpledialog.askinteger("ID Usuario", "Introduce tu ID de usuario:")
    if not idusuario:
        messagebox.showerror("Error", "ID de usuario inválido")
        return

    contenido = simpledialog.askstring("Comentario", "Escribe tu comentario:")
    if not contenido:
        messagebox.showerror("Error", "El comentario no puede estar vacío")
        return

    if lst_comentarios.curselection():
        idx = lst_comentarios.curselection()[0]
        if messagebox.askyesno("Respuesta", "¿Es respuesta a este comentario?"):
            comentarios = cargar_comentarios(idnoticia)
            idcomentario_respuesta = comentarios[idx].idcomentario
            guardar_comentario(idnoticia, idusuario, contenido, idcomentario_respuesta)
            messagebox.showinfo("Éxito", "Respuesta agregada")
            mostrar_comentarios(idnoticia)
            return

    guardar_comentario(idnoticia, idusuario, contenido)
    messagebox.showinfo("Éxito", "Comentario agregado")
    mostrar_comentarios(idnoticia)

frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

btn_add_noticia = tk.Button(frame_botones, text="Agregar Noticia (solo interno)", command=agregar_noticia)
btn_add_noticia.pack(side='left', padx=5)

btn_add_comentario = tk.Button(frame_botones, text="Agregar Comentario/Respuesta", command=agregar_comentario)
btn_add_comentario.pack(side='left', padx=5)

lst_noticias.bind('<<ListboxSelect>>', mostrar_noticia)

actualizar_noticias()

root.mainloop()
