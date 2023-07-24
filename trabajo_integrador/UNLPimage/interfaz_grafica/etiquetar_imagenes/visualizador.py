import PySimpleGUI as sg
import os.path
import PIL.Image
import sys
import datetime
from ...paths import IMAGENES, DATABASE, RUTA_BASE, BOTONES, IMAGENES_ETIQUETADAS
from .funciones import cargar_configuracion, verificar_archivo, guardar_datos, buscar_datos, mostrar_detalles_imagen, verificar_metadata
from ...log.src import event_log

boton_guardar = os.path.join(BOTONES,"button_guardar.png")
boton_salir = os.path.join(BOTONES,"button_salir.png")
boton_ver_detalles = os.path.join(BOTONES,"button_ver-detalles.png")

def obtener_informacion_imagen(filename):
    """
    Obtiene información de una imagen dada su filename.
    Args: filename (str): Ruta y nombre de archivo de la imagen.
    Returns: Tuple[str, str, str, str]: Ruta, tamaño, resolución y tipo de la imagen.
    """
    statinfo = os.stat(filename)
    ruta = os.path.dirname(filename)
    resolucion = f"{statinfo.st_size} bytes"
    with PIL.Image.open(filename) as img:
        tamaño = f"{img.size[0]} x {img.size[1]}"
    tipo = os.path.splitext(filename)[1]
    return ruta, tamaño, resolucion, tipo

def cargar_imagen_datos(nombre_imagen):
    """
    Carga los datos de una imagen desde la base de datos.
    Args: nombre_imagen (str): Nombre de la imagen.
    Returns: Tuple[str, str]: Descripción y tags de la imagen.
    """
    imagen_data = buscar_datos(nombre_imagen)
    if imagen_data:
        descripcion = imagen_data.get("descripcion", "")
        tags = imagen_data.get("tags", "")
    else:
        descripcion = ""
        tags = ""
    return descripcion, tags


def main_visualizador(perfil, ruta_collage=None, imagen_inicial=None):
    """
    Función principal del visualizador de imágenes.
    Args: perfil (str): Perfil de usuario.
    Returns: None
    """

    # Verifica la existencia del archivo
    verificar_archivo()

    #Cargamos configuracion de la ruta de imagenes
    ruta_elegida = cargar_configuracion('ruta_imagen')
    RUTA_FOTOS = os.path.join(IMAGENES, ruta_elegida)

    file_list_column = [
        [sg.Text("Dir. de Imágenes")],
        [sg.Combo(values=[file for file in os.listdir(RUTA_FOTOS) if file.lower().endswith(".png")], enable_events=True, readonly=True, size=(45, 15),
                  default_value=imagen_inicial or "Seleccionar imagen", key="-FILE_COMBO-", disabled=(imagen_inicial and ruta_collage) is not None)],
        [sg.Text('Descripción:'), sg.Input('', size=(45, 15), key='-DESCRIPCION-')],
        [sg.Text('Tags:'), sg.Input('', size=(45, 15), key='-TAGS-')],
        [sg.Text('Los tags deben estar separados por coma.', text_color=('grey'))],
        [sg.Button('', image_filename=boton_guardar, key='-GUARDAR-', button_color=('White', sg.theme_background_color())),
         sg.Button('', image_filename=boton_ver_detalles, key='-DETALLES-', button_color=('White', sg.theme_background_color())),
         sg.Button('', image_filename=boton_salir, key='-SALIR-', button_color=('White', sg.theme_background_color()))]
    ]

    image_viewer_column = [
        [sg.Text('Elija una imagen', key='-NOMBRE-')],
        [sg.Image(key="-IMAGE-", filename=os.path.join(RUTA_FOTOS, imagen_inicial) if imagen_inicial else None)],
    ]

    layout = [
        [sg.Text('UNLPImage', font=("Helvetica", 16), justification='left')],
        [sg.Column(file_list_column), sg.VSeparator(), sg.Column(image_viewer_column)]
    ]

    window = sg.Window("Visualizador", layout, text_justification="center", size=(900, 600))

    # Variable para determinar si el usuario guardó los datos cuando viene desde collage.
    guardar_requerido = False
    
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            window.close()
            sys.exit()

        if event == '-SALIR-':
            # Si viene desde colage, debe guardar.
            if ((imagen_inicial and ruta_collage) is not None) and not guardar_requerido:
                sg.popup('Debe guardar sus cambios.')
            else: 
                break

        if event == "-FILE_COMBO-":
            try:
                filename = os.path.join(RUTA_FOTOS, values["-FILE_COMBO-"])

                # Verificamos que realmente sea un .png la imagen seleccionada
                if verificar_metadata(filename):
                    # Si es, obtenemos su información
                    window['-NOMBRE-'].update(os.path.basename(filename))
                    nombre_imagen = os.path.basename(filename)
                    window["-IMAGE-"].update(filename=filename, size=(500, 500))
                    ruta, tamaño, resolucion, tipo = obtener_informacion_imagen(filename)
                    descripcion, tags = cargar_imagen_datos(nombre_imagen)
                    window['-DESCRIPCION-'].update(descripcion)
                    window['-TAGS-'].update(tags)
                else:
                # Si no es, mostramos un mensaje
                    window["-IMAGE-"].update(filename=None)
                    window['-NOMBRE-'].update('Elija una imagen')
                    window["-FILE_COMBO-"].update('Seleccionar imagen')
                    window['-DESCRIPCION-'].update('')
                    window['-TAGS-'].update('')
                    sg.popup('La imagen no es válida.')
            except Exception as e:
                sg.PopupQuickMessage("Error al abrir la imagen.")

                
        if event == '-DETALLES-':
            if window["-FILE_COMBO-"] != 'Seleccionar imagen':
                # Acciones cuando la imagen viene desde la ventana collage
                if (imagen_inicial and ruta_collage) != None:
                    filename = os.path.join(RUTA_FOTOS, values["-FILE_COMBO-"])
                    ruta, tamaño, resolucion, tipo = obtener_informacion_imagen(filename)
                    descripcion, tags = cargar_imagen_datos(imagen_inicial)
                    mostrar_detalles_imagen(imagen_inicial, ruta, tamaño, resolucion, tipo, descripcion, tags)
                else:
                    # Acción normal de etiquetado
                    if 'filename' in locals():
                        mostrar_detalles_imagen(nombre_imagen, ruta, tamaño, resolucion, tipo, descripcion, tags)
            else:
                # No puede ver los detalles de una imagen no seleccionada
                sg.popup('Debe seleccionar una imagen.')

        if event == '-GUARDAR-':
            # Acciones cuando la imagen viene desde la ventana collage
            if (imagen_inicial and ruta_collage) != None:
                nombre_actual = values['-FILE_COMBO-']
                descripcion = window['-DESCRIPCION-'].get()
                tags = window['-TAGS-'].get()
                ruta_absoluta = os.path.relpath(ruta_collage, IMAGENES)
                ruta_absoluta = str(ruta_absoluta.split('/')[0]) # Profe no juzgues esto, fue una decisión desesperada
                ruta, tamaño, resolucion, tipo = obtener_informacion_imagen(ruta_collage)
                guardar_datos(perfil, nombre_actual, ruta_absoluta, resolucion, tamaño, tipo, perfil, datetime.datetime.now(), descripcion, tags)
                sg.popup_quick_message('Se ha guardado la información.')
                guardar_requerido = True
            else:
                # Acción normal de etiquetado
                if 'filename' in locals():
                    descripcion = window['-DESCRIPCION-'].get()
                    tags = window['-TAGS-'].get()
                    ruta_absoluta = os.path.relpath(ruta, IMAGENES)
                    guardar_datos(perfil, nombre_imagen, ruta_absoluta, resolucion, tamaño, tipo, perfil, datetime.datetime.now(), descripcion, tags)
                    sg.popup_quick_message('Se ha guardado la información.')
    window.close()