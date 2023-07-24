import PySimpleGUI as sg
import os 
import json
import sys
import subprocess
from .directorio_collages import main_collage
from .directorio_memes import main_meme
from .directorio_imagenes import main_imagen
from ...paths import DATABASE, BOTONES, ESTADISTICAS


boton_salir = os.path.join(BOTONES,"button_salir.png")
boton_memes = os.path.join(BOTONES,"button_directorio-memes.png")
boton_collages = os.path.join(BOTONES,"button_directorio-collages.png")
boton_imagenes = os.path.join(BOTONES,"button_directorio-imagenes.png")


ESTRUCTURA_JSON = {
    "ruta_collage": "elija/su/ruta",
    "ruta_memes": "elija/su/ruta",
    "ruta_imagen": "elija/su/ruta"
}

def verificar_archivo_json():
    """
    Verificamos la existencia del archivo, sino lo creamos con la estructura determinada
    """
    RUTA_JSON = os.path.join(DATABASE, 'config.json')

    if not os.path.isfile(RUTA_JSON):
        with open(RUTA_JSON, 'w') as archivo:
            json.dump(ESTRUCTURA_JSON, archivo, indent=4)


def main_configuracion(perfil):
    """
    recibe un perfil
    Abre la ventana de configuración con diferentes opciones para el perfil especificado.

    - Muestra una interfaz con botones para diferentes opciones de configuración (imágenes, collages, memes).
    - Al hacer clic en el botón de collages, llama a la función `main_collage` para el perfil especificado.
    - Al hacer clic en el botón de memes, llama a la función `main_meme` para el perfil especificado.
    - Al hacer clic en el botón de imágenes, llama a la función `main_imagen` para el perfil especificado.
    - Al hacer clic en el botón de salir o cerrar la ventana, finaliza la función.

    """
    
    # Generamos layout de la estrucutura general
    layout = [[sg.Button('', image_filename=boton_imagenes, button_color=('White', sg.theme_background_color()),  key='-IMAGEN-', pad=(0,10)),],
              [sg.Button('', image_filename=boton_collages, button_color=('White', sg.theme_background_color()),  key='-COLLAGE-', pad=(0,10))],
              [sg.Button('', image_filename=boton_memes, button_color=('White', sg.theme_background_color()),  key='-MEMES-', pad=(0,10))],
              [sg.Button('', image_filename=boton_salir,button_color=('White',sg.theme_background_color()),key='-SALIR-', pad=(0,100))],
              ]

    # Creamos ventana
    window = sg.Window('Configuración', layout,size=(900, 600), margins=(100, 100),
                       element_justification='center')

    verificar_archivo_json()

    # Iniciamos la ventana
    while True:
        evento, valor = window.read()

        if evento == sg.WINDOW_CLOSED:
            window.close()
            sys.exit()

        if evento == '-SALIR-':
            break
        
        elif evento == '-COLLAGE-':
            window.hide()
            main_collage(perfil)
            window.un_hide()

        elif evento == '-MEMES-':
            window.hide()
            main_meme(perfil)
            window.un_hide()

        elif evento == '-IMAGEN-':
            window.hide()
            main_imagen(perfil)
            window.un_hide()

    window.close()