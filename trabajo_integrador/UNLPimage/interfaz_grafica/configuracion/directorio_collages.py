import PySimpleGUI as sg
import os
import json
from ...paths import DATABASE, COLLAGE, IMAGENES
from ...log.src import event_log


PATH_CONFIG = os.path.join(DATABASE,'config.json')

def main_collage(perfil):
    """
    recibe un perfil.
    Gestiona la elección del directorio de collages para el perfil especificado.

    - Carga la información del archivo JSON de configuración.
    - Muestra una ventana para que el usuario elija un directorio.
    - Al hacer clic en el botón 'Ok', guarda el directorio elegido en el archivo de configuración.
    - Registra la operación de modificar el directorio de collages en un registro de eventos.
    - Muestra un mensaje emergente de éxito al guardar la elección.
    - Al hacer clic en el botón 'Cancel' o cerrar la ventana, se finaliza la función.

    """

    # Creamos la variable para registrar eventos
    logger = event_log.EventLogger()


    # Cargar información del archivo JSON
    with open(PATH_CONFIG, 'r') as f:
            config = json.load(f)


    # Nos guardamos la ruta que eligió el usuario por última vez
    ruta_elegida = config.get('ruta_collage', '')

    # Organizacion ventana
    layout = [[sg.Text('Directorio')],
                [sg.InputText(default_text=ruta_elegida, key='-RUTA_COLLAGE-'), sg.FolderBrowse('Elegir carpeta',initial_folder=IMAGENES)],
                [sg.Button('Ok',key='-GUARDAR_COLLAGE-'), sg.Button('Cancel',key='-VOLVER_COLLAGE-')]]

    #Creamos ventana
    window = sg.Window('Configuración - Elección de directorio de collages',
                        layout, size=(None, None), margins=(90, 90))


    # Iniciamos ventana
    while True:
        evento, valor = window.read()

        if evento == sg.WIN_CLOSED:
            break

        if evento == '-GUARDAR_COLLAGE-':
            EVENTO = 'Modificar directorio de collages'
            logger.log_operation(perfil, EVENTO)

            # Nos guardamos el valor que ingresa el usuario
            ruta = valor['-RUTA_COLLAGE-']

            # Nos gurdamos la ruta relativa
            ruta_elegida = os.path.relpath(ruta,IMAGENES)

            config['ruta_collage'] = ruta_elegida
            with open(PATH_CONFIG, 'w') as f:
                json.dump(config, f,indent=4)

            sg.PopupQuickMessage('Guardado con éxito')

        elif evento == '-VOLVER_COLLAGE-':
                window.close()

    window.close()