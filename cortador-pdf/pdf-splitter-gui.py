import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if archivo:
        entrada_archivo.delete(0, tk.END)
        entrada_archivo.insert(0, archivo)

def dividir_pdf():
    archivo_entrada = entrada_archivo.get()
    if not archivo_entrada:
        messagebox.showerror("Error", "Por favor seleccione un archivo PDF")
        return

    directorio_salida = filedialog.askdirectory()
    if not directorio_salida:
        return

    try:
        pdf = PdfReader(archivo_entrada)
        for i in range(len(pdf.pages)):
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf.pages[i])
            
            output_filename = os.path.join(directorio_salida, f'pagina_{i+1}.pdf')
            with open(output_filename, 'wb') as out:
                pdf_writer.write(out)
        
        messagebox.showinfo("Éxito", f"El PDF ha sido dividido en {len(pdf.pages)} archivos")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Divisor de PDF")
ventana.geometry("400x150")

# Crear y colocar los widgets
tk.Label(ventana, text="Seleccione el archivo PDF:").pack(pady=5)
entrada_archivo = tk.Entry(ventana, width=50)
entrada_archivo.pack(pady=5)

boton_seleccionar = tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo)
boton_seleccionar.pack(pady=5)

boton_dividir = tk.Button(ventana, text="Dividir PDF", command=dividir_pdf)
boton_dividir.pack(pady=10)

# Iniciar el bucle principal
ventana.mainloop()
