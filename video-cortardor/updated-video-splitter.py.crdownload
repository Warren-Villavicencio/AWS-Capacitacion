import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import json

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'default_output_dir': '', 'default_fragment_size': 80}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def dividir_video(video_path, output_dir, tamaño_fragmento_mb, formato_nombre="fragmento_{}.mp4"):
    """
    Divide un video en fragmentos de un tamaño máximo especificado y los guarda en el directorio seleccionado.
    """
    video = VideoFileClip(video_path)
    duracion_total = video.duration
    tamaño_total = os.path.getsize(video_path) / (1024 * 1024)  # Tamaño en MB
    
    num_fragmentos = max(1, int(tamaño_total / tamaño_fragmento_mb))
    duracion_fragmento = duracion_total / num_fragmentos

    nombre_base, extension = os.path.splitext(os.path.basename(video_path))

    for i in range(num_fragmentos):
        inicio = i * duracion_fragmento
        fin = min((i + 1) * duracion_fragmento, duracion_total)
        clip = video.subclip(inicio, fin)
        
        nombre_archivo = os.path.join(output_dir, formato_nombre.format(i+1))
        clip.write_videofile(nombre_archivo, codec="libx264")

    video.close()

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv")])
    entrada_archivo.delete(0, tk.END)
    entrada_archivo.insert(0, archivo)

def seleccionar_carpeta_salida():
    carpeta = filedialog.askdirectory()
    entrada_carpeta_salida.delete(0, tk.END)
    entrada_carpeta_salida.insert(0, carpeta)

def iniciar_division():
    video_path = entrada_archivo.get()
    output_dir = entrada_carpeta_salida.get()
    tamaño_fragmento = int(entrada_tamaño.get())

    if not video_path or not os.path.exists(video_path):
        messagebox.showerror("Error", "Por favor, seleccione un archivo de video válido.")
        return

    if not output_dir or not os.path.exists(output_dir):
        messagebox.showerror("Error", "Por favor, seleccione un directorio de salida válido.")
        return

    try:
        nombre_base, extension = os.path.splitext(os.path.basename(video_path))
        formato_nombre = f"{nombre_base}_parte_{{:03d}}{extension}"
        dividir_video(video_path, output_dir, tamaño_fragmento, formato_nombre)
        messagebox.showinfo("Éxito", "El video ha sido dividido correctamente.")

        # Guardar la configuración actual
        config = load_config()
        config['default_output_dir'] = output_dir
        config['default_fragment_size'] = tamaño_fragmento
        save_config(config)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al dividir el video: {str(e)}")

# Cargar la configuración
config = load_config()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Divisor de Videos")
ventana.geometry("600x300")

# Crear y colocar los widgets
tk.Label(ventana, text="Archivo de video:").pack()
entrada_archivo = tk.Entry(ventana, width=50)
entrada_archivo.pack()
tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo).pack()

tk.Label(ventana, text="Carpeta de salida:").pack()
entrada_carpeta_salida = tk.Entry(ventana, width=50)
entrada_carpeta_salida.insert(0, config['default_output_dir'])
entrada_carpeta_salida.pack()
tk.Button(ventana, text="Seleccionar carpeta", command=seleccionar_carpeta_salida).pack()

tk.Label(ventana, text="Tamaño máximo de fragmento (MB):").pack()
entrada_tamaño = tk.Entry(ventana, width=10)
entrada_tamaño.insert(0, str(config['default_fragment_size']))
entrada_tamaño.pack()

tk.Button(ventana, text="Dividir video", command=iniciar_division).pack()

ventana.mainloop()
