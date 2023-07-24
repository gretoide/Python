import json
import os
import PySimpleGUI as sg
from ..perfil import nuevo_perfil
from ..menu_principal import menu_principal
from ...paths import RUTA_BASE , IMAGENES, FOTOS_DE_PERFIL, BOTONES
from PIL import Image


PATH_JSON = os.path.join(RUTA_BASE, 'database', 'datos.json')
FOTOS_PERFIL = os.path.join(IMAGENES, 'fotos_de_perfil')

agregar_perfil = os.path.join(BOTONES,"button_agregar-perfil.png")
ver_mas = os.path.join(BOTONES,"button_ver-mas.png")
salir = os.path.join(BOTONES,"button_salir.png")
seleccionar = os.path.join(BOTONES,"button_seleccionar.png")

# Lee los perfiles desde el archivo JSON
def cargar_perfiles():
    """
    Carga los perfiles desde un archivo JSON.

    Intenta cargar los perfiles desde un archivo JSON especificado por PATH_JSON.
    Si el archivo no existe, crea un nuevo archivo y devuelve una lista vacía.

    Returns:
    - perfiles: Lista de perfiles cargados desde el archivo JSON o una lista vacía.

    """
    try:
        perfiles = json.load(open(PATH_JSON, "r+"))
    except FileNotFoundError:
        perfiles = []
        json.dump(perfiles, open(PATH_JSON, "w+"))
    return perfiles

def mostrar_perfiles(perfiles, inicio=0, cantidad=4):
    """Muestra los perfiles en la ventana de inicio"""

    perfil_buttons = [
        sg.Button(
            image_filename=os.path.join(FOTOS_DE_PERFIL, perfil['Avatar']),
            key=f"perfil_{i}",
            size=(10, 1),pad=(30,50),
            button_color=('white', sg.theme_background_color()),
        )
        for i, perfil in enumerate(perfiles[:4])
    ]
    if len(perfiles) > inicio + cantidad:
        perfil_buttons.append(sg.Button('', image_filename=ver_mas, key='--VER-MAS--', font=("Helvetica", 10), button_color=('White',sg.theme_background_color())))
    if len(perfiles) == 0:
        perfil_buttons = [sg.Text('No hay perfiles creados', key='--NO-HAY-PERFILES--')]
    return perfil_buttons

def mostrar_todos_los_perfiles(perfiles):
    """Muestra todos los perfiles disponibles en una nueva ventana"""
    layout = [
        [sg.Text('Selecciona un perfil', font=("Helvetica", 10))],
        [sg.Listbox(values=[perfil['Alias'] for perfil in perfiles[4:]], size=(30, 6), key='perfil_list')],
        [sg.Button('',image_filename=seleccionar, key='--SELECCIONAR--', size=(10, 1), button_color=('White',sg.theme_background_color())),
         sg.Button('',image_filename=salir, key='--CANCELAR--', size=(10, 1), button_color=('White',sg.theme_background_color()))],
        ]

    # Crea la ventana
    window_plus = sg.Window('UNLPImage', layout, element_justification='center')
    perfil_seleccionado = None

    # Ejecuta el loop principal de la ventana
    while True:
        event, values = window_plus.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '--SELECCIONAR--':
            perfil_seleccionado = values['perfil_list'][0]
            break
        elif event == '--CANCELAR--':
            break
        
    window_plus.close()
    return perfil_seleccionado

def main_vinicio():
    """
    Función principal que muestra la ventana inicial y maneja los eventos.

    La función configura el tema y la fuente de la aplicación, carga los perfiles existentes y muestra la interfaz
    inicial. Maneja los eventos de los botones y realiza acciones correspondientes según el evento seleccionado.

    """
    # Cambiar el tema predeterminado para toda la aplicación
    sg.change_look_and_feel('LightGreen6')

    # Establecer la fuente predeterminada para toda la aplicación
    sg.set_options(font=('Helvetica', 10),border_width=0)

    perfiles = cargar_perfiles()

    layout = [
    [sg.Text('UNLPimage', justification='center', font=("Helvetica", 16))],
    [
        sg.Column(
            [
                mostrar_perfiles(perfiles)
            ],
            justification='center',
            element_justification='center',
            pad=(0,90)
        )
    ],
    [
        sg.Column(
            [
                [
                    sg.Button('', image_filename=agregar_perfil, key='--AGREGAR--', button_color=('White',sg.theme_background_color())),
                    sg.Button('', image_filename=salir, key='--SALIR--', button_color=('White',sg.theme_background_color()))
                ]
            ],
            justification='center',
            element_justification='center',
            pad=(0, 30)
        )
    ]
    ]


    # Crea la ventana
    window = sg.Window('UNLPmage', layout,size=(900, 600))

    # Ejecuta el loop principal de la ventana
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '--SALIR--':
            break
        elif event == '--AGREGAR--':
            window.hide()
            nuevo_perfil.main_nuevo_perfil()
            window.close()
            main_vinicio()
            
        elif event == '--VER-MAS--':

            perfil_seleccionado = mostrar_todos_los_perfiles(perfiles)
            
            if perfil_seleccionado is not None:
                # Obtener los datos completos del perfil seleccionado
                perfil_completo = next((perfil for perfil in perfiles if perfil['Alias'] == perfil_seleccionado), None)
                
                if perfil_completo is not None:
                    # Guardar los datos del perfil seleccionado en la variable PERFIL_SELECCIONADO
                    PERFIL_SELECCIONADO = {
                        'Alias': perfil_completo['Alias'],
                        'Nombre': perfil_completo['Nombre'],
                        'Fecha de nacimiento': perfil_completo['Fecha de nacimiento'],
                        'Sexo': perfil_completo['Sexo'],
                        'Avatar': perfil_completo['Avatar']
                    }
                    window.close()
                    menu_principal.main(PERFIL_SELECCIONADO)
                    main_vinicio()
                    
        elif event.startswith('perfil_'):
            window.hide()
            perfil_index = int(event.split('_')[1])
            perfil_seleccionado = perfiles[perfil_index]['Alias']
            # Obtener los datos completos del perfil seleccionado
            perfil_completo = next((perfil for perfil in perfiles if perfil['Alias'] == perfil_seleccionado), None)
           
            if perfil_completo is not None:
                
                # Guardar los datos del perfil seleccionado en la variable PERFIL_SELECCIONADO
                PERFIL_SELECCIONADO = {
                    'Alias': perfil_completo['Alias'],
                    'Nombre': perfil_completo['Nombre'],
                    'Fecha de nacimiento': perfil_completo['Fecha de nacimiento'],
                    'Sexo': perfil_completo['Sexo'],
                    'Avatar': perfil_completo['Avatar']
                }
                window.hide()
                menu_principal.main(PERFIL_SELECCIONADO)
                window.un_hide()
