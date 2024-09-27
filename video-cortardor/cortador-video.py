import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip

def dividir_video(video_path, tamaño_fragmento_mb=80, formato_nombre="fragmento_{}.mp4"):
    """
    Divide un video en fragmentos de un tamaño máximo especificado y personaliza los nombres de los archivos.

    Args:
        video_path (str): Ruta al video original.
        tamaño_fragmento_mb (int): Tamaño máximo de cada fragmento en megabytes.
        formato_nombre (str): Formato de nombre para los archivos de salida.
            Se utiliza la sintaxis de format para incluir un número de secuencia.
    """
    video = VideoFileClip(video_path)
    duracion_total = video.duration
    tamaño_total = os.path.getsize(video_path) / (1024 * 1024)  # Tamaño en MB
    
    # Calcular el número de fragmentos
    num_fragmentos = max(1, int(tamaño_total / tamaño_fragmento_mb))
    duracion_fragmento = duracion_total / num_fragmentos

    directorio_base = os.path.dirname(video_path)
    nombre_base, extension = os.path.splitext(os.path.basename(video_path))

    for i in range(num_fragmentos):
        inicio = i * duracion_fragmento
        fin = min((i + 1) * duracion_fragmento, duracion_total)
        clip = video.subclip(inicio, fin)
        
        nombre_archivo = os.path.join(directorio_base, formato_nombre.format(i+1))
        clip.write_videofile(nombre_archivo, codec="libx264")

    video.close()

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")])
    entrada_archivo.delete(0, tk.END)
    entrada_archivo.insert(0, archivo)

def iniciar_division():
    video_path = entrada_archivo.get()
    tamaño_fragmento = 80  # Fijamos el tamaño máximo a 80 MB

    if not video_path or not os.path.exists(video_path):
        messagebox.showerror("Error", "Por favor, seleccione un archivo de video válido.")
        return

    try:
        nombre_base, extension = os.path.splitext(os.path.basename(video_path))
        formato_nombre = f"{nombre_base}_parte_{{:03d}}{extension}"
        dividir_video(video_path, tamaño_fragmento, formato_nombre)
        messagebox.showinfo("Éxito", "El video ha sido dividido correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al dividir el video: {str(e)}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Divisor de Videos")
ventana.geometry("600x200")

# Crear y colocar los widgets
tk.Label(ventana, text="Archivo de video:").pack()
entrada_archivo = tk.Entry(ventana, width=50)
entrada_archivo.pack()
tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo).pack()

tk.Label(ventana, text="El video se dividirá en partes de máximo 80 MB").pack()

tk.Button(ventana, text="Dividir video", command=iniciar_division).pack()

ventana.mainloop()
