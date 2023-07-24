from PIL import Image
import os

ruta_actual = os.path.abspath(os.path.dirname(__file__))

def resize_images_in_folder(folder_path, new_size):
    # Obtener la lista de archivos en la carpeta
    files = os.listdir(folder_path)

    for file_name in files:
        # Comprobar si el archivo es una imagen
        if file_name.endswith(".png") or file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
            # Ruta completa del archivo
            image_path = os.path.join(folder_path, file_name)

            # Abrir la imagen original
            image = Image.open(image_path)

            # Redimensionar la imagen
            resized_image = image.resize(new_size)

            # Guardar la imagen redimensionada
            resized_image.save(image_path)

# Tamaño deseado (100x100 píxeles)
tamaño_nuevo = (50, 50)

# Llamar a la función para redimensionar todas las imágenes en la carpeta actual
resize_images_in_folder(ruta_actual, tamaño_nuevo)