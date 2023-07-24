import PySimpleGUI as sg
import os
import csv
import sys
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from ..configuracion import configuracion_llamado
from ..etiquetar_imagenes import visualizador
from ..etiquetar_imagenes.funciones import cargar_configuracion, verificar_archivo, verificar_metadata
from ...paths import BOTONES, DATABASE, IMAGENES, FUENTES, IMAGENES_ETIQUETADAS
from ...log.src import event_log

PATH_FUENTE = os.path.join(FUENTES,'roboto_regular.ttf')

# Rutas de los archivos de datos
DATOS_IMAGENES = os.path.join(DATABASE, 'datos_imagenes.csv')
guardar = os.path.join(BOTONES, "button_guardar.png")
salir = os.path.join(BOTONES, "button_salir.png")

def verificar_longitud(texto):
    """
    Recibe un texto y verifica que no supere los 25 caracteres.
    """
    if texto != None:
        if len(texto) <= 25:
            return True
        else:
            return False


def agregar_imagen(ruta_imagen, lienzo, posicion_x, posicion_y):
    """
    recibe ruta de imagen, lienzo y coordenadas de posicion.
    Agrega una imagen al lienzo.
    """
    imagen = Image.open(ruta_imagen)
    lienzo.paste(imagen, (posicion_x, posicion_y))

def agregar_titulo(texto, lienzo):
    """
    recibe el texto y lienzo.
    Agrega un título al lienzo (imagen) proporcionado.
    El título se coloca en la esquina inferior derecha del lienzo,
    con un pequeño margen de 10 unidades en los bordes.
    """
    ancho_lienzo, alto_lienzo = lienzo.size
    fuente = ImageFont.truetype(PATH_FUENTE, 20)
    dibujo = ImageDraw.Draw(lienzo)
    texto_ancho, texto_alto = dibujo.textsize(texto, font=fuente)
    posicion_x = ancho_lienzo - texto_ancho - 10
    posicion_y = alto_lienzo - texto_alto - 10

    # Dibujar cuadro negro de fondo
    cuadro_x1 = posicion_x - 5
    cuadro_y1 = posicion_y - 5
    cuadro_x2 = ancho_lienzo - 10
    cuadro_y2 = alto_lienzo - 10
    dibujo.rectangle([(cuadro_x1, cuadro_y1), (cuadro_x2, cuadro_y2)], fill=(0, 0, 0))

    # Dibujar texto en blanco
    dibujo.text((posicion_x, posicion_y), texto, fill=(255, 255, 255), font=fuente)

def actualizar_vista_previa(lienzo):
    """
    recibe lienzo.
    Actualiza la vista previa del lienzo.
    """
    lienzo_redimensionado = lienzo.resize((500, 500))
    imagen_bytes = BytesIO()
    lienzo_redimensionado.save(imagen_bytes, format='PNG')
    return imagen_bytes.getvalue()

def crear_lienzo_vacio(ancho, alto):
    """
    recibe ancho y alto.
    Crea un lienzo vacío con el ancho y alto especificados.
    """
    lienzo = Image.new('RGB', (ancho, alto), (255, 255, 255))
    return lienzo

def existe_imagen(nombre_imagen):
    """
    recibe el nombre de imagen.
    Verifica si una imagen con el nombre dado existe en el archivo CSV de datos.
    """
    with open(DATOS_IMAGENES, mode='r', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if row['imagen'] == nombre_imagen:
                return True
        return False

def verificar_etiquetado(archivo, perfil, window, text_boxes=None, boton_numero=None, lienzo=None ):
    """
    Verifica si la imagen seleccionada está etiquetada.
    
    - Obtiene el nombre del archivo de imagen.
    - Verifica si la imagen está etiquetada en función de su nombre.
    - Si la imagen no está etiquetada, muestra un cuadro de diálogo para preguntar si se desea etiquetarla.
    - Si se elige etiquetarla y no se ha configurado una ruta de imágenes, llama a la función `llamar_configuracion` para el perfil.
    - Si se elige etiquetarla y se ha configurado una ruta de imágenes, llama a la función `main_visualizador` para mostrar la imagen y etiquetarla.
    - Posiciona la imagen en el lienzo y actualiza la vista previa del collage.
    - Si la imagen está etiquetada, retorna True.

    """
    # Verificamos el archivo
    verificar_archivo()

    # Verificamos la ruta
    ruta_configurada = cargar_configuracion('ruta_imagen')

    # Verificamos el etiquetado de la imagen y en caso de no estarlo, llamamos a la función para etiquetarla
    nombre = os.path.basename(archivo)
    if not existe_imagen(nombre):
        respuesta = sg.popup_yes_no('La imagen aún no ha sido etiquetada, ¿desea etiquetarla?')

        # Si la respuesta es afirmativa, llamamos a la función para etiquetar la imagen
        if respuesta == 'Yes':
            # Si no se ha configurado una ruta de imágenes, llamamos a la función para configurarla
            if ruta_configurada == "elija/su/ruta" or ruta_configurada is None:
                window.hide()
                configuracion_llamado.llamar_configuracion(perfil)
                window.un_hide()
            else:
            # Si se ha configurado una ruta de imágenes, llamamos a la función para etiquetar la imagen
                window.hide()
                visualizador.main_visualizador(perfil, archivo, nombre)
                # Posicionar imagen en el lienzo
                posicionar_imagen(archivo, text_boxes, boton_numero, lienzo)
                # Agregar una imagen con los datos para su posicionamiento y tamaño
                window['-COLLAGE-'].update(data=actualizar_vista_previa(lienzo))
                window.un_hide()
        else:
            sg.popup('Debera elegir una imagen que esté etiqueda')
    else:
        return True

def posicionar_imagen(archivo, text_boxes, boton_numero, lienzo):
    """
    Posiciona una imagen en el lienzo según las coordenadas proporcionadas.
    """
    if archivo:
        # Verificar la extensión del archivo seleccionado
        extension = os.path.splitext(archivo)[1].lower()
        # Guardamos coordenada correspondiente al botón
        tipo_imagen_json = text_boxes[boton_numero]
        # Las asignamos
        ancho = tipo_imagen_json["top_left_x"]
        alto = tipo_imagen_json["top_left_y"]
        ancho_hasta = tipo_imagen_json["bottom_right_x"]
        alto_hasta = tipo_imagen_json["bottom_right_y"]
        recorte_x = ancho_hasta - ancho
        recorte_y = alto_hasta - alto
        # Actualizamos
        imagen = Image.open(archivo)
        imagen = imagen.resize((recorte_x, recorte_y))
        imagen_bytes = BytesIO()
        imagen.save(imagen_bytes, format='PNG')
        agregar_imagen(imagen_bytes, lienzo, ancho, alto)

def main_seleccionar_imagen(perfil, cantidad, text_boxes):
    """
    Función principal para seleccionar y posicionar imágenes en un collage.
    """

    # Cargamos la ruta de las imágenes donde se encuentran las fotos para hacer collage
    ruta_imagenes = cargar_configuracion('ruta_imagen')
    RUTA_FOTOS = os.path.join(IMAGENES, ruta_imagenes)

    # Creamos la ruta donde se van a guardar los collage generados
    ruta_collage = cargar_configuracion('ruta_collage')
    RUTA_COLLAGES = os.path.join(IMAGENES, ruta_collage)


    # Creamos la variable para registrar eventos
    logger = event_log.EventLogger()
    ancho_plantilla = 500
    alto_plantilla = 500

    # Creamos variable para almacenar imágenes utilizadas en collage
    value_event = []

    # Creamos el lienzo
    lienzo = crear_lienzo_vacio(ancho_plantilla, alto_plantilla)

    vista_previa = [
        [sg.Frame('Collage', [
            [sg.Image(data=actualizar_vista_previa(lienzo), key='-COLLAGE-')]
        ], size=(500, 500))]
    ]

    titulo = [
        [sg.Input('Titulo', key='-TITULO-')],
    ]

    seleccion_imagen = [
        [sg.Button(f'Seleccionar imagen {str(i+1)}', key=f'-SELECCION-{i}-')] for i in range(cantidad)
    ]

    botones = [
        [sg.Button('', image_filename=guardar, button_color=('White', sg.theme_background_color()), key='-GUARDAR-'),
         sg.Button('', image_filename=salir, button_color=('White', sg.theme_background_color()), key='-SALIR-')]
    ]

    layout = [
        [sg.Column(titulo)],
        [sg.Column(seleccion_imagen, pad=(0, 120)), sg.VSeparator(),
         sg.Column(vista_previa)],
        [sg.Column(botones)]
    ]

    window = sg.Window('Creación collage', layout, size=(900, 600), element_justification='center')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            window.close()
            sys.exit()

        if event == '-SALIR-':
            break

        if event.startswith('-SELECCION-'):
            try:
                boton_numero = int(event.split('-')[2])

                # Verificamos la existencia del CSV.
                verificar_archivo()

                archivo = sg.popup_get_file('Seleccionar imagen', file_types=(('PNG Files', '*.png'),), initial_folder=RUTA_FOTOS)

                # Verificar que la imagen seleccionada sea un verdadero .png
                if verificar_metadata(archivo):
                    if archivo != None:
                        # Verificar etiquetado
                        if verificar_etiquetado(archivo, perfil, window, text_boxes, boton_numero, lienzo):

                            # Posicionar imagen en el lienzo
                            posicionar_imagen(archivo, text_boxes, boton_numero, lienzo)

                            # Agregar una imagen con los datos para su posicionamiento y tamaño
                            window['-COLLAGE-'].update(data=actualizar_vista_previa(lienzo))    

                            # Guardamos el nombre de la imagen
                            value_event.append(os.path.basename(archivo))

                    else:
                        sg.PopupQuickMessage('No se seleccionó ninguna imagen.')
                else:
                    sg.Popup("La imagen seleccionada no es válida")
            except TypeError:
                sg.PopupQuickMessage('No se seleccionó ninguna imagen.')

        if event == '-GUARDAR-':

            # Verificamos que el título no sea demasiado largo
            if not verificar_longitud(values['-TITULO-']):
                sg.PopupQuickMessage('El título debe contener menos de 25 caracteres.')
            else:
                # Procedemos a guardar el archivo
                try:
                    nombre_archivo = sg.popup_get_text('Ingrese el nombre del archivo', 'Guardar Collage')
                    if not verificar_longitud(nombre_archivo): # Verificamos que el nombre no sea demasiado largo
                        sg.PopupQuickMessage('El nombre del archivo debe contener menos de 25 caracteres y no puede estar vacío.')
                    else:
                        # Verificamos que la ruta de guardado exista y si es asó, guardamos el archivo
                        if nombre_archivo != '':
                            # Registramos el evento
                            text_events = values['-TITULO-']
                            logger.log_operation(perfil, "Nuevo Collage", value_event, text_events)

                            # Guardamos la imagen
                            titulo_texto = values['-TITULO-']
                            agregar_titulo(titulo_texto, lienzo)
                            ruta_guardado_completa = os.path.join(RUTA_COLLAGES, f'{nombre_archivo}.png')
                            try:
                                lienzo.save(ruta_guardado_completa)
                                sg.popup('Collage guardado exitosamente.')
                                # Actualizamos la vista previa
                                window['-COLLAGE-'].update(ruta_guardado_completa)

                            except OSError:
                                sg.popup('El nombre del archivo tiene caracteres inválidos o la ruta no fue configurada.')
                                break
                            
                        else:
                            sg.popup('Debe ingresar un nombre para el archivo.')
                            continue
                except FileNotFoundError:
                    sg.popup('La ruta de guardado no existe o no fue configurada.')
                    continue

            
    window.close()