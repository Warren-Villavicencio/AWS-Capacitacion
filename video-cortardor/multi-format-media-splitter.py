import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip, AudioFileClip
from PIL import Image
import json

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'default_output_dir': '', 'default_fragment_size': 80, 'default_output_format': 'mp4'}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def process_media(input_path, output_dir, tamaño_fragmento_mb, output_format, formato_nombre):
    """
    Procesa el archivo de entrada y lo divide en fragmentos del formato especificado.
    """
    _, input_extension = os.path.splitext(input_path)
    input_extension = input_extension.lower()

    if input_extension in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
        clip = VideoFileClip(input_path)
    elif input_extension in ['.mp3', '.wav', '.ogg', '.flac']:
        clip = AudioFileClip(input_path)
    else:
        raise ValueError(f"Formato de entrada no soportado: {input_extension}")

    duracion_total = clip.duration
    tamaño_total = os.path.getsize(input_path) / (1024 * 1024)  # Tamaño en MB
    
    num_fragmentos = max(1, int(tamaño_total / tamaño_fragmento_mb))
    duracion_fragmento = duracion_total / num_fragmentos

    for i in range(num_fragmentos):
        inicio = i * duracion_fragmento
        fin = min((i + 1) * duracion_fragmento, duracion_total)
        sub_clip = clip.subclip(inicio, fin)
        
        nombre_archivo = os.path.join(output_dir, formato_nombre.format(i+1))

        if output_format in ['mp4', 'avi', 'mov', 'mkv']:
            sub_clip.write_videofile(f"{nombre_archivo}.{output_format}")
        elif output_format in ['mp3', 'wav', 'ogg']:
            sub_clip.audio.write_audiofile(f"{nombre_archivo}.{output_format}")
        elif output_format in ['jpg', 'png']:
            frame = sub_clip.get_frame(0)  # Get the first frame
            im = Image.fromarray(frame)
            im.save(f"{nombre_archivo}.{output_format}")
        else:
            raise ValueError(f"Formato de salida no soportado: {output_format}")

    clip.close()

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[
        ("Todos los archivos soportados", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.mp3 *.wav *.ogg *.flac"),
        ("Archivos de video", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
        ("Archivos de audio", "*.mp3 *.wav *.ogg *.flac")
    ])
    entrada_archivo.delete(0, tk.END)
    entrada_archivo.insert(0, archivo)

def seleccionar_carpeta_salida():
    carpeta = filedialog.askdirectory()
    entrada_carpeta_salida.delete(0, tk.END)
    entrada_carpeta_salida.insert(0, carpeta)

def iniciar_proceso():
    input_path = entrada_archivo.get()
    output_dir = entrada_carpeta_salida.get()
    tamaño_fragmento = int(entrada_tamaño.get())
    output_format = combo_formato.get()

    if not input_path or not os.path.exists(input_path):
        messagebox.showerror("Error", "Por favor, seleccione un archivo de entrada válido.")
        return

    if not output_dir or not os.path.exists(output_dir):
        messagebox.showerror("Error", "Por favor, seleccione un directorio de salida válido.")
        return

    try:
        nombre_base, _ = os.path.splitext(os.path.basename(input_path))
        formato_nombre = f"{nombre_base}_parte_{{:03d}}"
        process_media(input_path, output_dir, tamaño_fragmento, output_format, formato_nombre)
        messagebox.showinfo("Éxito", "El archivo ha sido procesado correctamente.")

        # Guardar la configuración actual
        config = load_config()
        config['default_output_dir'] = output_dir
        config['default_fragment_size'] = tamaño_fragmento
        config['default_output_format'] = output_format
        save_config(config)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al procesar el archivo: {str(e)}")

# Cargar la configuración
config = load_config()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Procesador de Medios Multiformato")
ventana.geometry("600x350")

# Crear y colocar los widgets
tk.Label(ventana, text="Archivo de entrada:").pack()
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

tk.Label(ventana, text="Formato de salida:").pack()
formatos_salida = ['mp4', 'avi', 'mov', 'mkv', 'mp3', 'wav', 'ogg', 'jpg', 'png']
combo_formato = ttk.Combobox(ventana, values=formatos_salida)
combo_formato.set(config['default_output_format'])
combo_formato.pack()

tk.Button(ventana, text="Procesar archivo", command=iniciar_proceso).pack()

ventana.mainloop()
