import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

TEMP_DIR = "Temp"

def ensure_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((400, 400))  # Уменьшаем изображение для отображения
        label.original_image = img.convert("RGB")  # Преобразуем в RGB
        label.file_path = file_path
        update_compressed_image()

def update_compressed_image(*args):
    if hasattr(label, 'original_image'):
        quality = int(quality_scale.get())  # Преобразуем в int
        temp_path = os.path.join(TEMP_DIR, "temp_compressed.jpg")
        label.original_image.save(temp_path, 'JPEG', quality=quality)
        img = Image.open(temp_path)
        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk

def save_compressed_image():
    if hasattr(label, 'original_image'):
        quality = int(quality_scale.get())  # Преобразуем в int
        output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if output_path:
            label.original_image.save(output_path, 'JPEG', quality=quality)
            print(f"Изображение сохранено в {output_path} с качеством {quality}.")

ensure_temp_dir()

app = tk.Tk()
app.title("JPEG Compressor")

# Используем ttk для улучшения внешнего вида
style = ttk.Style(app)
style.theme_use('clam')  # Выбираем тему

frame = ttk.Frame(app, padding="10 10 10 10")
frame.pack(fill=tk.BOTH, expand=True)

open_button = ttk.Button(frame, text="Открыть изображение", command=open_image)
open_button.pack(pady=5)

label = ttk.Label(frame)
label.pack(pady=5)

quality_label = ttk.Label(frame, text="Качество:")
quality_label.pack(pady=5)

quality_scale = ttk.Scale(frame, from_=1, to=95, orient=tk.HORIZONTAL, command=update_compressed_image)
quality_scale.set(85)
quality_scale.pack(fill=tk.X, pady=5)

save_button = ttk.Button(frame, text="Сохранить сжатое изображение", command=save_compressed_image)
save_button.pack(pady=5)

app.mainloop()
