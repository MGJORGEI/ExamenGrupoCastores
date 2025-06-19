# ExamenGrupoCastores
# Sistema de Noticias — App Escritorio en Python

## ¿Qué es esto?

Este programa es una app de escritorio para manejar noticias dentro de una empresa. La idea es simple:  
- Solo el personal interno puede subir noticias.  
- Cualquier usuario (interno o externo) puede comentar esas noticias.  
- Y sí, también pueden responder comentarios, para que la plática fluya.  

Todo con su fecha y quién lo hizo, porque el detalle importa.

La app está hecha en Python usando `pyodbc` para conectar con SQL Server y `tkinter` para la interfaz gráfica, así que es liviana y fácil de correr.

---

## ¿Qué necesito para correr esto?

- Tener instalado Python 3.11 (o superior) en Windows (es la que recomiendo, yo uso la 3.11).  
- Tener SQL Server con la base de datos 
- El driver ODBC 17 para conectar Python con SQL Server (instálalo desde la página de Microsoft, está fácil).  
- Instalar el módulo `pyodbc` con pip (te explico cómo justo aquí abajo).  
- `tkinter` ya viene con Python, así que nada extra ahí.

---

## Paso a paso para poner todo a correr

1. **Instala Python** desde [python.org](https://www.python.org/downloads/windows/).  
2. **Instala ODBC Driver 17** desde [Microsoft](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).  
3. Abre PowerShell y corre:

   ```bash
   pip install pyodbc

