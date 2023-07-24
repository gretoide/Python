from PIL import Image, ImageDraw, ImageOps
import os
import string
import random
from ...paths import FOTOS_DE_PERFIL

def redimensionar_imagen(imagen_ruta):
    """
    Redimensiona una imagen a 50x50 píxeles, aplica un marco redondo y la guarda en una ubicación específica.
    """
    # Cargar la imagen
    imagen = Image.open(imagen_ruta)
    
    # Redimensionar la imagen a 100x100
    imagen_redimensionada = imagen.resize((50, 50))
    
    # Crear un lienzo transparente del mismo tamaño de la imagen redimensionada
    lienzo = Image.new('RGBA', imagen_redimensionada.size, (0, 0, 0, 0))
    
    # Crear una máscara de círculo
    mascara = Image.new('L', imagen_redimensionada.size, 0)
    dibujo = ImageDraw.Draw(mascara)
    dibujo.ellipse((0, 0, imagen_redimensionada.size[0], imagen_redimensionada.size[1]), fill=255)
    
    # Aplicar la máscara al lienzo
    lienzo.paste(imagen_redimensionada, (0, 0), mask=mascara)
    
    # Obtener el nombre base de la imagen original
    nombre_base = os.path.basename(imagen_ruta)
    
     # Obtener la ruta completa de destino
    ruta_destino = os.path.join(FOTOS_DE_PERFIL, nombre_base)
    
    # Guardar la imagen con marco redondo en la ruta completa de destino
    lienzo.save(ruta_destino)

    return ruta_destino