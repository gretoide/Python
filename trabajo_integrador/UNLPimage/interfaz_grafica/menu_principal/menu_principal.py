import PySimpleGUI as sg
import sys
import os
import subprocess
from ..generar_memes import generador_de_memes
from ..generar_collage import collage_principal
from ..configuracion import configuracion, configuracion_llamado
from ..etiquetar_imagenes.visualizador import main_visualizador
from ..etiquetar_imagenes.funciones import cargar_configuracion
from ..perfil import editar_perfil
from ...paths import RUTA_BASE, FOTOS_DE_PERFIL, ICONOS, BOTONES, ESTADISTICAS, DATABASE

RUTA_SREAMLIT = os.path.join(ESTADISTICAS,'ventana_principal.py')
RUTA_CSV = os.path.join(DATABASE,'datos_imagenes.csv')
RUTA_CSV_LOGS = os.path.join(RUTA_BASE,'log','event_log.csv')

salir = os.path.join(BOTONES,'button_salir.png')
boton_editar_perfil = os.path.join(BOTONES,'button_editar-perfil.png')
icono_collage = os.path.join(ICONOS,'collage.png')
icono_memes = os.path.join(ICONOS,'meme.png')
icono_etiquetar = os.path.join(ICONOS,'etiquetar.png')
icono_configuracion = os.path.join(ICONOS,'configuracion.png')
icono_ayuda = os.path.join(ICONOS,'informacion.png')
icono_estadisticas = os.path.join(ICONOS,'estadisticas.png')

def open_streamlit():
    """Abre la ventana de estadísticas."""
    subprocess.Popen(["streamlit", "run", RUTA_SREAMLIT])


def verificar_datos(datos_imagenes_path, log_events_path):
    """Verifica la existencia de los archivos datos_imagenes.csv y log_events.csv"""
    if os.path.exists(datos_imagenes_path) and os.path.exists(log_events_path):
        open_streamlit()
    else:
        sg.popup("Advertencia: Poca información disponible para generar estadísticas.", title="Alerta")

def mostrar_popup_datos_perfil(window,perfil):
    """Muestra un popup con los datos del perfil"""
    layout = [
        [sg.Image(filename=(os.path.join(FOTOS_DE_PERFIL, perfil['Avatar'])))],
        [sg.Text(f"Alias: {perfil['Alias']}")],
        [sg.Text(f"Nombre: {perfil['Nombre']}")],
        [sg.Text(f"Fecha de nacimiento: {perfil['Fecha de nacimiento']}")],
        [sg.Text(f"Sexo: {perfil['Sexo']}")],
        [sg.Button('',image_filename=boton_editar_perfil, button_color=('White', sg.theme_background_color()), key='--EDITAR--')]
    ]

    window_popup = sg.Window('Datos del Perfil', layout, modal=True)
    while True:
        event, _ = window_popup.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '--EDITAR--':
            window.hide()
            window_popup.close()
            perfil = editar_perfil.main_eperfil(perfil)
            window.un_hide()
            break
    return perfil

def mensaje_ayuda():
    """Muestra un mensaje de ayuda con información sobre las opciones disponibles."""
    texto = (
    "Bienvenido al sistema de ayuda.\n"
    "\n"
    "Aquí encontrarás información sobre las diferentes opciones disponibles.\n"
    "\n"
    "PERFIL: Muestra los datos del perfil seleccionado.\n"
    "ETIQUETAR: Abre la interfaz para etiquetar una imagen.\n"
    "MEME: Abre el generador de memes.\n"
    "COLLAGE: Abre el creador de collages.\n"
    "CONFIGURACIÓN: Abre la configuración.\n"
    "AYUDA: Muestra este mensaje de ayuda.\n"
    "SALIR: Cierra la aplicación.\n"
    "\n"
    "Para editar la información del perfil seleccionado:\n"
    "\n"
    "1. Haz clic en la foto de tu perfil\n"
    "2. Se abrirá una ventana con los datos del perfil\n"
    "3. Click en el botón - Editar Perfil\n"
    "4. Se abrirá una ventana con los datos que pueden editarse y a continuación puede guardar o cancelar dichos cambios"
    )

    sg.popup(texto, title='Ayuda', font=('Helvetica', 12, 'bold'))



def main(PERFIL_SELECCIONADO):
    """
    Función principal que muestra la interfaz principal y maneja los eventos.

    Parámetros:
    - PERFIL_SELECCIONADO: Diccionario que contiene los datos del perfil seleccionado.

    La función crea la ventana principal con diferentes botones para acceder a las opciones del sistema.
    Maneja los eventos de los botones y realiza acciones correspondientes según el evento seleccionado.
    Permite editar el perfil, etiquetar imágenes, generar memes, generar collages, acceder a la configuración,
    ver la ayuda y salir de la aplicación.
    """
        
    # Boton foto de perfil
    perfil_columna = [
        [sg.Button(image_filename=(os.path.join(FOTOS_DE_PERFIL, PERFIL_SELECCIONADO['Avatar'])), key="-PERFIL-", button_color=('White', sg.theme_background_color()))],
    ]

    # Botón Etiquetar
    boton_etiquetar = sg.Column([
        [sg.Button("", key="-ETIQUETAR-", image_filename=icono_etiquetar, button_color=('White', sg.theme_background_color()))],
        [sg.Text("Etiquetar imágenes", justification='center', font=('Helvetica', 12, 'bold'))]
    ], element_justification='center',pad=(20,0))

    # Botón Crear Meme
    boton_meme = sg.Column([
        [sg.Button("", key="-MEME-", image_filename=icono_memes, button_color=('White', sg.theme_background_color()))],
        [sg.Text("Crear meme", justification='center', font=('Helvetica', 12, 'bold'))]
    ], element_justification='center',pad=(20,0))

    # Botón Crear Collage
    boton_collage = sg.Column([
        [sg.Button("", key="-COLLAGE-", image_filename=icono_collage, button_color=('White', sg.theme_background_color()))],
        [sg.Text("Crear collage", justification='center', font=('Helvetica', 12, 'bold'))]
    ], element_justification='center',pad=(20,0))

    # Columna de botones
    menu_columna = [
        [boton_etiquetar,boton_collage,boton_meme,]
    ]

    boton_salir = [
            sg.Button("", image_filename=salir, key="-SALIR-", button_color=('White', sg.theme_background_color()), size=(10, 1), pad=(5, 5))
    ]

    configuracion_columna = [
        [
        sg.Button("", key="-CONFIGURACION-", image_filename=icono_configuracion, button_color=('White', sg.theme_background_color())), 
        sg.Button("", key="-AYUDA-",image_filename=icono_ayuda, button_color=('White', sg.theme_background_color())),
        sg.Button("", key="-ESTADISTICAS-", image_filename=icono_estadisticas, button_color=('White', sg.theme_background_color()))],
    ]

    layout = [
        [
            sg.Column([[sg.Column(perfil_columna)]], element_justification='left', pad=((0, 350), 0)),
            sg.Column([[sg.Column(configuracion_columna)]], element_justification='right',  pad=((300, 0), 0))
        ],
        [
            sg.Column([[sg.Column(menu_columna)]], justification='center', element_justification='center', pad=((0, 40), 120))
        ],
        [
            sg.Column([boton_salir],element_justification='center')
        ]
    ]

    window = sg.Window("UNLPimage", layout, size=(900,600), element_justification="center")


    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED:
            window.close()
            sys.exit()

        if event == '-SALIR-':
            break
        
        elif event == "-PERFIL-":
            PERFIL_SELECCIONADO = mostrar_popup_datos_perfil(window,PERFIL_SELECCIONADO)
            window['-PERFIL-'].update(image_filename=(os.path.join(FOTOS_DE_PERFIL, PERFIL_SELECCIONADO['Avatar'])))

        elif event == "-ETIQUETAR-":
            ruta_configurada = cargar_configuracion('ruta_imagen')
            if ruta_configurada == "elija/su/ruta" or ruta_configurada == None: 
                window.hide()
                configuracion_llamado.llamar_configuracion(PERFIL_SELECCIONADO['Alias'])
                window.un_hide()

            else:
                window.hide()
                main_visualizador(PERFIL_SELECCIONADO['Alias'])
                window.un_hide()

        elif event == "-MEME-":
            ruta_configurada = cargar_configuracion('ruta_memes')
            if ruta_configurada == "elija/su/ruta" or ruta_configurada is None:
                window.hide()
                configuracion_llamado.llamar_configuracion(PERFIL_SELECCIONADO['Alias'])
                window.un_hide()
            else:
                window.hide()
                generador_de_memes.main_generador_de_memes(PERFIL_SELECCIONADO['Alias'])
                window.un_hide()

        elif event == "-COLLAGE-":
            ruta_configurada = cargar_configuracion('ruta_imagen')
            if ruta_configurada == "elija/su/ruta" or ruta_configurada is None:
                window.hide()
                configuracion_llamado.llamar_configuracion(PERFIL_SELECCIONADO['Alias'])
                window.un_hide()
            else:
                window.hide()
                collage_principal.main_collage(PERFIL_SELECCIONADO['Alias'])
                window.un_hide()

        elif event == "-CONFIGURACION-":
            window.hide()
            configuracion.main_configuracion(PERFIL_SELECCIONADO['Alias'])
            window.un_hide()

        elif event == "-AYUDA-":
            mensaje_ayuda()

        elif event == "-ESTADISTICAS-":
            verificar_datos(RUTA_CSV, RUTA_CSV_LOGS)

    window.close()
