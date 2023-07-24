import os
import csv
import PySimpleGUI as sg
from PIL import Image
import json
from ...paths import DATABASE
from ...log.src import event_log

# Rutas de los archivos de datos
DATOS_IMAGENES = os.path.join(DATABASE,'datos_imagenes.csv')
CONFIG_JSON = os.path.join(DATABASE,'config.json')

def cargar_imagen_datos(nombre_imagen):
    """
    recibe una imagen.
    Carga los datos de una imagen desde el archivo CSV de datos.
    """
    imagen_data = buscar_datos(nombre_imagen)
    if imagen_data:
        descripcion = imagen_data.get("descripcion", "")
        tags = imagen_data.get("tags", [])
    else:
        descripcion = ""
        tags = []
    return descripcion, tags

def cargar_configuracion(nombre=None):
    """
    Carga la configuración de las rutas desde el archivo JSON.
    """
    if not os.path.isfile(CONFIG_JSON):
        sg.popup_ok("Configure la ruta de las imágenes en 'Configuración'.", title="Alerta")
        return None
    else:
        with open(CONFIG_JSON, 'r') as f:
            configuracion = json.load(f)
        return configuracion[nombre]

def verificar_archivo():
    """
    Verifica si el archivo CSV de datos existe y crea el encabezado si no existe.
    """
    if not os.path.exists(DATOS_IMAGENES):
        # Si el archivo no existe, se crea con el encabezado
        with open(DATOS_IMAGENES, "w", newline="") as archivo_csv:
            escritor_csv = csv.DictWriter(archivo_csv, fieldnames=["imagen", "ruta", "resolucion", "tamano", "tipo", "ultimo_perfil", "ultima_actualizacion", "descripcion","tags"], delimiter=";")
            escritor_csv.writeheader()
    else:
        # Si el archivo ya existe, no se hace nada
        pass

def existe_imagen(nombre_imagen):
    """
    Verifica si una imagen con el nombre dado existe en el archivo CSV de datos.
    Args: nombre_imagen (str): Nombre de la imagen.
    Returns: True si la imagen existe, False en caso contrario.
    """
    with open(DATOS_IMAGENES, mode='r', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if row['imagen'] == nombre_imagen:
                return True
        return False
    
def mostrar_detalles_imagen(nombre_imagen, ruta, tamaño, resolucion, tipo, descripcion, tags):
    """
    Muestra una ventana con los detalles de una imagen.
    """
    # Crear el layout
    layout = [
        [sg.Text("Nombre de la imagen:"), sg.Text(nombre_imagen)],
        [sg.Text("Ruta:"), sg.Text(ruta)],
        [sg.Text("Tamaño:"), sg.Text(tamaño)],
        [sg.Text("Resolución:"), sg.Text(resolucion)],
        [sg.Text("Tipo:"), sg.Text(tipo)],
        [sg.Text("Descripción:"), sg.Text(descripcion)],
        [sg.Text("Tags:"), sg.Text(tags)],
    ]

    # Crear la ventana
    window = sg.Window("Detalles de la imagen", layout)

    # Mostrar la ventana y esperar eventos
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

    # Cerrar la ventana al salir del loop
    window.close()


def guardar_datos(perfil, imagen, ruta, resolucion, tamano, tipo, ultimo_perfil, ultima_actualizacion, descripcion, tags):
    """
    Guarda los datos de una imagen en el archivo CSV de datos.
    Si la imagen ya existe, se actualizan los campos, de lo contrario se agrega una nueva fila.
    """
    logger = event_log.EventLogger()
    if existe_imagen(imagen):
        # Si la imagen ya existe, se actualizan los campos
        datos = []
        with open(DATOS_IMAGENES, mode='r', newline='') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                if row['imagen'] == imagen:
                    row['ruta'] = ruta
                    row['resolucion'] = resolucion
                    row['tamano'] = tamano
                    row['tipo'] = tipo
                    row['ultimo_perfil'] = ultimo_perfil
                    row['ultima_actualizacion'] = ultima_actualizacion
                    row['descripcion'] = descripcion
                    row['tags'] = tags
                datos.append(row)

        with open(DATOS_IMAGENES, mode='w', newline='') as file:
            NOMBRES_CAMPOS = ['imagen', 'ruta', 'resolucion', 'tamano', 'tipo', 'ultimo_perfil', 'ultima_actualizacion', 'descripcion', 'tags']
            writer = csv.DictWriter(file, fieldnames=NOMBRES_CAMPOS, delimiter=';')
            writer.writeheader()
            writer.writerows(datos)
            logger.log_operation(perfil, "Modificacion de imagen previamente clasificada", imagen, [descripcion, tags])

    else:
        # Si la imagen no existe, se agrega una nueva fila
        with open(DATOS_IMAGENES, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([imagen, ruta, resolucion, tamano, tipo, ultimo_perfil, ultima_actualizacion, descripcion, tags])
            logger.log_operation(perfil, "Nueva imagen etiquetada", imagen, [descripcion, tags])

def buscar_datos(nombre_imagen):
    """
    Busca los datos de una imagen en el archivo CSV de datos.
    """
    with open(DATOS_IMAGENES, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            if row["imagen"] == nombre_imagen:
                return row
    return None

def datos_imagen_info(filename):
    """
    Obtiene la información de una imagen dada su filename.
    """
    statinfo = os.stat(filename)
    ruta_absoluta = os.path.dirname(filename)
    ruta_relativa = os.path.relpath(ruta_absoluta)
    resolucion = f"{statinfo.st_size} bytes"
    with Image.open(filename) as img:
        tamaño = f"{img.size[0]} x {img.size[1]}"
        tipo = os.path.splitext(filename)[1]
    return ruta_relativa, tamaño, resolucion, tipo

def buscar_descripcion_tags(nombre_imagen):
    """
    Busca la descripción y los tags de una imagen en el archivo CSV de datos.
    """
    with open(DATOS_IMAGENES, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            if row["imagen"] == nombre_imagen:
                tags = row.get("tags", "")
                descripcion = row.get("descripcion", "")
                return tags, descripcion
    return "", ""


def verificar_metadata(imagen):
    """
    Verifica si la imagen es un verdadero PNG.
    """
    if os.path.isfile(imagen):
        imagen_pillow = Image.open(imagen)
        if imagen_pillow.format == "PNG":
            return True
        else:
            return False
