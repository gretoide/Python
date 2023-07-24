import os
import json
import sys
import PySimpleGUI as sg
from ...paths import RUTA_BASE, IMAGENES, DATABASE, COLLAGE_TEMPLATES, BOTONES
from ...paths import ICONOS
from .seleccion_imagenes import main_seleccionar_imagen

BOTON_SALIR = os.path.join(BOTONES, "button_salir.png")
DOS_COLLAGE = os.path.join(ICONOS,"dos_collage.png")
TRES_COLLAGE = os.path.join(ICONOS,"tres_collage.png")
CUATRO_COLLAGE = os.path.join(ICONOS,"cuatro_collage.png")
CINCO_COLLAGE = os.path.join(ICONOS,"cinco_collage.png")


COLLAGES = os.path.join(COLLAGE_TEMPLATES,'collage.json')

def cargar_plantillas():
    """
    Carga las plantillas del archivo JSON y las retorna como una lista de diccionarios
    """
    with open(COLLAGES, "r") as archivo:
        data = json.load(archivo)
        plantillas = data["collage_templates"]
    return plantillas

def obtener_coordenadas_plantilla(nombre_plantilla):
    """
    Retorna las coordenadas de una plantilla específica según su nombre
    """
    plantillas = cargar_plantillas()
    for plantilla in plantillas:
        if plantilla["nombre_plantilla"] == nombre_plantilla:
            coordenadas = plantilla["coordenadas"]
            return coordenadas
    return None

def main_collage(perfil):
    """
    Se selecciona la plantilla a utilizar para el collage
    """

    templates = cargar_plantillas()

    boton_dos = sg.Column([
        [sg.Button("", key="-DOS-", image_filename=DOS_COLLAGE, button_color=('White', sg.theme_background_color()))]
    ])

    boton_tres = sg.Column([
        [sg.Button("", key="-TRES-", image_filename=TRES_COLLAGE, button_color=('White', sg.theme_background_color()))]
    ])

    boton_cuatro = sg.Column([
        [sg.Button("", key="-CUATRO-", image_filename=CUATRO_COLLAGE, button_color=('White', sg.theme_background_color()))]
    ])

    boton_cinco = sg.Column([
        [sg.Button("", key="-CINCO-", image_filename=CINCO_COLLAGE, button_color=('White', sg.theme_background_color()))]
    ])

    opciones_collage = [
        [boton_dos, boton_tres, boton_cuatro, boton_cinco],
        [sg.Button('', image_filename=BOTON_SALIR, button_color=('White', sg.theme_background_color()), key='-SALIR-',pad=((0, 0), (120, 0)))]
    ]

    layout = [
        [sg.Column(opciones_collage, element_justification='center', pad=((220, 0), (220, 0)))],
    ]

    ventana = sg.Window('Selector plantillas', layout, size=(900, 600))

    while True:
            evento, valores = ventana.read()

            if evento == sg.WINDOW_CLOSED:
                ventana.close()
                sys.exit()

            if evento == '-SALIR-':
                break

            if evento == '-DOS-':
                ventana.hide()
                text_boxes = obtener_coordenadas_plantilla('Dos imagenes')
                main_seleccionar_imagen(perfil, len(text_boxes), text_boxes)
                ventana.un_hide()

            elif evento == '-TRES-':
                ventana.hide()
                text_boxes = obtener_coordenadas_plantilla('Tres imagenes')
                main_seleccionar_imagen(perfil, len(text_boxes), text_boxes)
                ventana.un_hide()

            elif evento == '-CUATRO-':
                ventana.hide()
                text_boxes = obtener_coordenadas_plantilla('Cuatro imagenes')
                main_seleccionar_imagen(perfil, len(text_boxes), text_boxes)
                ventana.un_hide()

            elif evento == '-CINCO-':
                ventana.hide()
                text_boxes = obtener_coordenadas_plantilla('Cinco imagenes')
                main_seleccionar_imagen(perfil, len(text_boxes), text_boxes)
                ventana.un_hide()

    ventana.close()