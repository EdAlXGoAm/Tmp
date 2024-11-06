
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageGrab
import pytesseract
import numpy as np
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\uif05375\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def paste_image():
    try:
        # Obtiene la imagen del portapapeles
        image = ImageGrab.grabclipboard()

        if isinstance(image, Image.Image):
            # Ajusta la imagen para mostrar en la ventana
            image.thumbnail((400, 400))
            img = ImageTk.PhotoImage(image)

            # Muestra la imagen en la etiqueta
            image_label.config(image=img)
            image_label.image = img

            img_ocr = np.array(image)
            norm_img = np.zeros((img_ocr.shape[0], img_ocr.shape[1]))
            img_ocr = cv2.normalize(img_ocr, norm_img, 0, 255, cv2.NORM_MINMAX)
            img_ocr = cv2.threshold(img_ocr, 100, 255, cv2.THRESH_BINARY)[1]
            img_ocr = cv2.GaussianBlur(img_ocr, (1, 1), 0)
            text = pytesseract.image_to_string(img_ocr)
            words = text.split("\n")
            print("\nTexto extraído:")
            for word in words:
                print(f'"{word.strip()}",')
        
        else:
            messagebox.showerror("Error", "No hay una imagen en el portapapeles")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo pegar la imagen: {e}")
        print(f"Error: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Pegar Imagen desde Portapapeles")

# Etiqueta para mostrar la imagen
image_label = tk.Label(root)
image_label.pack(padx=10, pady=10)

# Botón para pegar la imagen
paste_button = tk.Button(root, text="Pegar Imagen", command=paste_image)
paste_button.pack(padx=10, pady=10)

# Iniciar el loop de la aplicación
root.mainloop()
