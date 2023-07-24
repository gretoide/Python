import os

# Rutas generales
RUTA_BASE = os.path.abspath(os.path.dirname(__file__))

# Database
DATABASE = os.path.join(RUTA_BASE,'database')

# Ruta Fuentes
FUENTES = os.path.join(DATABASE,'fonts')

# Interfaz gráfica
INTERFAZ_GRAFICA = os.path.join(RUTA_BASE,'interfaz_grafica')

# Rutas imágenes
COLLAGE_TEMPLATES = os.path.join(DATABASE,'collage_templates')

MEMES_TEMPLATES = os.path.join(DATABASE,'memes_templates')

IMAGENES = os.path.join(RUTA_BASE,'imagenes')

IMAGENES_ETIQUETADAS = os.path.join(IMAGENES,"fotos_etiquetadas")

FOTOS_DE_PERFIL = os.path.join(IMAGENES,"fotos_de_perfil")

COLLAGE = os.path.join(IMAGENES,"collage")

COLLAGE_GENERADOS = os.path.join(IMAGENES,'collage_generados')

MEMES = os.path.join(IMAGENES,"memes")

ICONOS = os.path.join(IMAGENES,"iconos")

ESTADISTICAS = os.path.join(RUTA_BASE,"estadisticas")

IMAGENES_ESTADISTICAS = os.path.join(DATABASE,"estadisticas","imagenes_graficos")

# Botones
BOTONES = os.path.join(IMAGENES,"iconos","botones")

IMAGENES_ESTADISTICAS = os.path.join(DATABASE,'estadisticas','imagenes_graficos')
