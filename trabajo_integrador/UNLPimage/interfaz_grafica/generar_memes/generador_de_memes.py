import os
import json
import sys
import PySimpleGUI as sg
from ...paths import RUTA_BASE, IMAGENES, DATABASE, MEMES_TEMPLATES, BOTONES
from .edicion_meme import main_editar_meme

salir = os.path.join(BOTONES,'button_salir.png')
boton_generar_meme = os.path.join(BOTONES,'button_generar-meme.png')
MEMES_GENERADOS = os.path.join(IMAGENES, 'memes_generados')
PLANTILLAS_MEMES = os.path.join(IMAGENES, 'plantillas_memes')

def cargar_archivos_plantillas():
    """
    Cargamos los archivos json dentro de una lista, para luego mostrarlos en el listado
    """
    templates = []
    # Leer todos los archivos JSON de plantillas dentro de la carpeta
    for archivo_json in os.listdir(MEMES_TEMPLATES):
        if archivo_json.endswith('.json'):
            ruta_json = os.path.join(MEMES_TEMPLATES, archivo_json)
            with open(ruta_json, 'r') as archivo:
                template = json.load(archivo)
                templates.append(template)

    return templates

def extract_json(templates, imagen_actual):
    """
    Extraemos del listado de JSON las coordenadas correspondiente a la imagen actual
    """
    for template in templates:
        if template[0]['image'] == imagen_actual: 
            return template[0]['text_boxes']
        

def main_generador_de_memes(perfil):
    """
    Genera la ventana de selección de plantilla  para nuestro meme
    """
    templates = cargar_archivos_plantillas()  # Cargar la lista de templates desde los archivos JSON

    # Crear un diccionario que mapee los nombres de las plantillas a las imágenes
    opciones = {template[0]['name']: template[0]['image'] for template in templates}

    # Crear una ventana con PySimpleGUI
    layout = [
        [sg.Text('Plantillas'), sg.Combo(
            list(opciones.keys()), size=(30, 70), key='-MENU-',readonly=True, default_value='Seleccionar Plantilla',  enable_events=True)],
        [sg.Frame('', [[sg.Image(key='-IMAGEN-', background_color='white')]], border_width=1, relief='sunken')],
        [sg.Button('',image_filename=boton_generar_meme, button_color=('White', sg.theme_background_color()), key='-GENERAR_MEME-'),
         sg.Button('',image_filename=salir, button_color=('White', sg.theme_background_color()), key='-SALIR-')],
    ]

    window = sg.Window('Generador de memes', layout,
                       size=(900, 600), finalize=True, element_justification='center')

    imagen_inicial = os.path.join(PLANTILLAS_MEMES, 'imagen_inicial', 'imagen_inicial.png')
    # Actualizar la vista previa con la imagen inicial
    window['-IMAGEN-'].update(filename=imagen_inicial)

    # Imagen actual que se está mostrando en la vista previa
    imagen_actual = imagen_inicial

    # Nombre de la plantilla actual
    nombre_plantilla = ''

    # Ciclo principal de la aplicación
    while True:
        evento, valor = window.read()
        
        if evento == sg.WINDOW_CLOSED:
            window.close()
            sys.exit()

        if evento == '-SALIR-':
            break
        
        # Elegimos imagen y se actualiza la vista previa
        if evento == '-MENU-':
            imagen_actual = os.path.join(PLANTILLAS_MEMES, opciones[valor['-MENU-']])

            # Adaptamos las imágenes al tamaño de la ventana
            window['-IMAGEN-'].update(filename=imagen_actual, size=(500, 500))

            text_boxes = extract_json(templates,opciones[valor['-MENU-']])

            nombre_plantilla = valor['-MENU-']

        if evento == '-GENERAR_MEME-':
            # Si no se eligió una plantilla, mostrar un mensaje de error
            if imagen_actual == imagen_inicial:
                sg.popup('Debe elegir una plantilla')
                continue

            # Cerrar la ventana actual y abrir la ventana de edición
            window.hide()
            main_editar_meme(perfil, len(text_boxes), imagen_actual, text_boxes, nombre_plantilla)
            window.un_hide()

    # Cerrar la ventana y salir del programa
    window.close()
