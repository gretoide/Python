import PySimpleGUI as sg
import os
from ...paths import ICONOS, BOTONES
from .configuracion import main_configuracion

icono_configuracion = os.path.join(ICONOS,'configuracion.png')
boton_salir = os.path.join(BOTONES,'button_salir.png')

def llamar_configuracion(perfil):
    """
    recibe un perfil 
    - Muestra una interfaz con opciones de configuración.
    - Al hacer clic en el botón de configuración, llama a la función `main_configuracion` con el perfil especificado.
    - Se cierra la ventana al hacer clic en el botón de salir o al cerrar la ventana.

    """
    layout = [
        [sg.Text('Alguno de sus repositorios no fue configurado.',pad=(0,120), font=('Helvetica',14))],
        [sg.Button('', image_filename=icono_configuracion, button_color=('White',sg.theme_background_color()), key="-BOTON-")],
        [sg.Button('', image_filename=boton_salir,button_color=('White',sg.theme_background_color()),key='-SALIR-', pad=(0,100))]
    ]

    # Crear la ventana
    window = sg.Window('Alerta', layout, element_justification='center', text_justification='center', size=(900,600))

    # Event Loop (bucle de eventos)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "-SALIR-":
            break

        if event == '-BOTON-':
            window.close()
            main_configuracion(perfil)
            
            
    # Cerrar la ventana al salir del bucle de eventos
    window.close()
