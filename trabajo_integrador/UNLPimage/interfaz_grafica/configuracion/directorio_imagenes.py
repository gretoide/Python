import PySimpleGUI as sg
import os
import json
from ...paths import DATABASE, IMAGENES
from ...log.src import event_log


PATH_CONFIG = os.path.join(DATABASE,'config.json')


def main_imagen(perfil):
    """
    recibe un perfil.
    Ejecuta la elección del directorio de imágenes para todos los perfiles.
    - Carga la información del archivo JSON de configuración.
    - Muestra una ventana para que el usuario elija un directorio de imágenes.
    - Al hacer clic en el botón 'Ok', guarda el directorio elegido en el archivo de configuración.
    - Registra la operación de modificar el directorio de imágenes en un registro de eventos.
    - Muestra un mensaje emergente de éxito al guardar la elección.
    - Al hacer clic en el botón 'Cancel' o cerrar la ventana, se finaliza la función.

    """

    # Creamos la variable para registrar eventos
    logger = event_log.EventLogger()

    # Cargar información del archivo JSON
    with open(PATH_CONFIG, 'r') as f:
            config = json.load(f)


    # Nos guardamos la ruta que eligió el usuario por última vez
    ruta_elegida = config.get('ruta_imagen', '')

    # Organizacion ventana
    layout = [[sg.Text('Directorio')],
                [sg.InputText(default_text=ruta_elegida, key='-RUTA_IMAGEN-'), sg.FolderBrowse('Elegir carpeta',initial_folder=IMAGENES)],
                [sg.Button('Ok',key='-GUARDAR_IMAGEN-'), sg.Button('Cancel',key='-VOLVER_IMAGEN-')]]

    #Creamos ventana
    window = sg.Window('Configuración - Elección de directorio de imagenes',
                        layout, size=(None, None), margins=(90, 90))


    # Iniciamos ventana
    while True:
        evento, valor = window.read()

        if evento == sg.WIN_CLOSED:
            break

        if evento == '-GUARDAR_IMAGEN-':
            EVENTO = 'Modificar directorio de imagenes'
            logger.log_operation(perfil, EVENTO)

            # Nos guardamos el valor que ingresa el usuario
            ruta = valor['-RUTA_IMAGEN-']

            # Nos gurdamos la ruta relativa
            ruta_elegida = os.path.relpath(ruta,IMAGENES)

            # Guardar información en el archivo JSON
            config['ruta_imagen'] = ruta_elegida
            with open(PATH_CONFIG, 'w') as f:
                json.dump(config, f,indent=4)

            sg.PopupQuickMessage('Guardado con éxito')

    
        elif evento == '-VOLVER_IMAGEN-':
                window.close()
    window.close()