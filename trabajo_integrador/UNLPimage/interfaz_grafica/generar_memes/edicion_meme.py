import PySimpleGUI as sg
import os
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont
from ...paths import FUENTES, BOTONES, IMAGENES, DATABASE
from ..etiquetar_imagenes.funciones import cargar_configuracion
from ...log.src import event_log
from ..configuracion.configuracion import verificar_archivo_json
from ..generar_collage.seleccion_imagenes import verificar_longitud

MEMES_PLANTILLAS = os.path.join(IMAGENES, 'plantillas_memes')
guardar = os.path.join(BOTONES,"button_guardar.png")
salir = os.path.join(BOTONES,"button_salir.png")
aplicar = os.path.join(BOTONES,"button_aplicar.png")

verificar_archivo_json()


def verificar_longitud_textos(textos):
    """
    Verifica que todos los textos tengan menos de 25 caracteres.
    """
    for texto in textos:
        if len(texto) > 25:
            return False
    return True

def tam_box(x1, y1, x2, y2):
    """
    Calculamos tamaño del BOX
    """
    return (x2 - x1, y2 - y1)

def entra(contenedor, contenido):
    """
    Verificamos si el texto entra
    """
    return contenido[0] <= contenedor[0] and contenido[1] <= contenedor[1]

def calcular_tam_fuente(draw, texto, path_fuente, box):
    """
    Usamos las funciones anteriores para verificar si el texto 
    ingresado entra en la casilla de texto
    """
    tam_contenedor = tam_box(*box)
    for tam in range(200, 20, -5):
        fuente = ImageFont.truetype(path_fuente, tam)
        box_texto = draw.textbbox((0, 0), texto, font=fuente)
        tam_box_texto = tam_box(*box_texto)
        if entra(tam_contenedor, tam_box_texto):
            return fuente

    return fuente

def main_editar_meme(perfil, cantidad, plantilla_original, template_pos, nombre_plantilla):
    """
    Apartado para editar el meme y rellenar las casillas de texto
    """

    # Se carga la ruta de las imagenes de memes
    ruta_elegida = cargar_configuracion('ruta_memes')
    RUTA_FOTOS = os.path.join(IMAGENES, ruta_elegida)

    # Creamos la variable para registrar eventos
    logger = event_log.EventLogger()

    fuentes_disponibles = [file for file in os.listdir(FUENTES)]
    seleccion_fuente = [
        [sg.Text('Fuente:'), sg.Combo(fuentes_disponibles, default_value="Seleccione Fuente", key='-FUENTE-', readonly=True)]
    ]

    seleccion_imagen = [
        [sg.Input(f'Texto {str(i+1)}', key=f'-TEXTO-{i}-', size=(20, 0))] for i in range(cantidad)
    ]

    seleccion_imagen.append([sg.Button('', key='-APLICAR-', image_filename=aplicar, button_color=('White',sg.theme_background_color()))])


    vista_previa = [
        [sg.Frame('', [[sg.Image(filename=plantilla_original, size=(600, 600), key='-IMAGEN-')]], border_width=1,
         relief='sunken')]
    ]

    botones = [
        [sg.Button('', image_filename=guardar, button_color=('White',sg.theme_background_color()), key='-GUARDAR_MEME-'), sg.Button('',image_filename=salir ,button_color=('White',sg.theme_background_color()), key='-SALIR-')]
    ]

    layout = [
        [sg.Column(seleccion_fuente, justification='center')],
        [sg.Column(seleccion_imagen, justification='center', element_justification='center'),
        sg.VSeparator(),
        sg.Column(vista_previa, justification='center')],
        [sg.Column(botones, justification='center')]
    ]
    window = sg.Window('Edición meme', layout, size=(1000, 700))

    while True:
        evento, valor = window.read()

        top_left_x, top_left_y, bottom_right_x, bottom_right_y = template_pos[0].values()

        # Creamos copia de la imagen
        meme_original = Image.open(plantilla_original)
        meme = meme_original.copy()
        draw = ImageDraw.Draw(meme)

        if evento == sg.WINDOW_CLOSED:
            window.close()
            sys.exit()

        if evento == '-SALIR-':
            break
        
        if evento == '-APLICAR-':
            ruta_temporal = os.path.join(tempfile.gettempdir(), 'temporal.png')

            # Verificar que se haya seleccionado una fuente
            if valor['-FUENTE-'] == 'Seleccione Fuente':
                sg.popup('Debe seleccionar una fuente.')
            else:
                # Verificar la longitud de los textos
                textos = [valor[f'-TEXTO-{i}-'] for i in range(cantidad) if valor[f'-TEXTO-{i}-']]
                if not verificar_longitud_textos(textos):
                    sg.popup('Uno o más textos superan los 25 caracteres.')
                else:
                    # Procedemos a procesar la imagen
                    fuente = os.path.join(FUENTES, valor['-FUENTE-'])

                    # Aplicar los cambios en la imagen
                    for i in range(cantidad):
                        texto = valor[f'-TEXTO-{i}-']
                        if texto:
                            top_left_x, top_left_y, bottom_right_x, bottom_right_y = template_pos[i].values()
                            fuente_ajustada = calcular_tam_fuente(draw, texto, fuente, (top_left_x, top_left_y, bottom_right_x, bottom_right_y))
                            # Aplicar los cambios
                            draw.text((top_left_x, top_left_y), texto, font=fuente_ajustada, fill=(0, 0, 0))

                    # Crear un archivo temporal para mostrar la imagen actualizada
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                        ruta_temporal = temp_file.name
                        meme.save(ruta_temporal)

                    # Mostrar la imagen actualizada en la vista previa
                    window['-IMAGEN-'].update(filename=ruta_temporal)

                    # La eliminamos luego de actualizar
                    if ruta_temporal:
                        os.remove(ruta_temporal)


        if evento == '-GUARDAR_MEME-':

            # Verificamos que se haya seleccionado una fuente
            if (valor['-FUENTE-'] == 'Seleccione Fuente'):
                sg.popup('Debe seleccionar una fuente.')
                continue

            # Asignamos la fuente seleccionada
            fuente = os.path.join(FUENTES, valor['-FUENTE-'])

            # Posicionamos los textos
            for i in range(cantidad):
                texto = valor[f'-TEXTO-{i}-']
                if texto:
                    top_left_x, top_left_y, bottom_right_x, bottom_right_y = template_pos[i].values()
                    fuente_ajustada = calcular_tam_fuente(draw, texto, fuente,
                                                          (top_left_x, top_left_y, bottom_right_x, bottom_right_y))
                    # Aplicamos los cambios
                    draw.text((top_left_x, top_left_y), texto, font=fuente_ajustada, fill=(0, 0, 0))

            # Guardamos el meme
            nombre_archivo = sg.popup_get_text('Ingrese el nombre del archivo', 'Guardar Meme')

            if (nombre_archivo is not '') and (verificar_longitud(nombre_archivo)): # Verificamos que el nombre no esté vacío
                
                # Registramos el evento
                value_event = nombre_plantilla
                text_events = ', '.join([valor[f'-TEXTO-{i}-'] for i in range(cantidad) if valor[f'-TEXTO-{i}-']])
                logger.log_operation(perfil, "Nuevo Meme", value_event, text_events)
                ruta_guardado_completa = os.path.join(RUTA_FOTOS, f'{nombre_archivo}.png')

                # Guardamos la imagen
                try:
                    meme.save(ruta_guardado_completa)
                    sg.PopupQuickMessage('Meme guardado existosamente.')
                except OSError:
                    sg.popup('El nombre del archivo tiene caracteres inválidos o la ruta no fue configurada.')
                    break

                # Actualizamos la vista previa
                window['-IMAGEN-'].update(ruta_guardado_completa)

            else:
                sg.popup('El nombre se encuentra vacío o supera los 25 caracteres.')
                continue

    window.close()