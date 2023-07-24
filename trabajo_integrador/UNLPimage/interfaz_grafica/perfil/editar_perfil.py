import PySimpleGUI as sg
import os
import json
import re
from .nuevo_perfil import main_nuevo_perfil,es_igual,verificar_archivo,campos_obligatorios,nombre_valido, verificar_longitud
from .resize import redimensionar_imagen
from ...paths import RUTA_BASE , DATABASE, IMAGENES, FOTOS_DE_PERFIL, ICONOS, BOTONES
from ...log.src import event_log
import sys

icono_calendario = os.path.join(ICONOS,'calendario.png')
carpeta_inicial = os.path.join(IMAGENES,'fotos_de_perfil')
archivo_json = os.path.join(DATABASE, 'datos.json')

opciones = ['Femenino','Masculino','Otro']

guardar = os.path.join(BOTONES,"button_guardar.png")
boton_avatar = os.path.join(BOTONES,"button_agregar-avatar.png")
salir = os.path.join(BOTONES,"button_salir.png")


def cargar_datos(nick, nombre, fecha, sexo, avatar):
    """ 
    Esta función abre el archivo JSON, busca el perfil a editar, permite su edición
    y luego lo guarda.
    """
    with open(archivo_json, "r+") as archivo:
        datos = json.load(archivo)

        # Buscar el nick en el JSON
        for perfil in datos:
            if perfil["Alias"] == nick:
                perfil["Alias"] = nick
                perfil["Nombre"] = nombre
                perfil["Fecha de nacimiento"] = fecha
                perfil["Sexo"] = sexo
                perfil["Avatar"] = os.path.basename(avatar)
                perfil_modificado = perfil
                break

        archivo.seek(0)  # Regresamos al inicio del archivo
        json.dump(datos, archivo, indent=4)  # Guardamos la lista actualizada en el archivo
        archivo.truncate()  # Eliminamos cualquier dato que quede a partir de la posición actual del archivo

    return perfil_modificado
    

def main_eperfil(perfil):
    """
        Se ejecuta la ventana principal de editar perfil.
    """

    logger = event_log.EventLogger()

    image_base = os.path.join(FOTOS_DE_PERFIL, perfil['Avatar'])

    columna_datos = [
        [sg.Text("Nick"), sg.Input(default_text=perfil["Alias"],key="-NICK-", size=(30, 30),disabled=True,text_color="#666666")],
        [sg.Text("Nombre"), sg.Input(default_text=perfil["Nombre"],key="-NOMBRE-", size=(30, 30))],
        [sg.Text("Fecha de nacimiento"),sg.InputText(default_text=perfil["Fecha de nacimiento"],key="-FECHA_NACIMIENTO-",disabled=True, text_color=('Black'), size=(10, 10)),
         sg.CalendarButton('', image_filename=icono_calendario,target="-FECHA_NACIMIENTO-", format='%Y-%m-%d',button_color=('White',sg.theme_background_color()))],
        [sg.Text("Genero"), sg.Combo(opciones, default_value=perfil["Sexo"],readonly=True, size=(30, 30), key='-GENERO-')],
    ]

    columna_botones = [
        [sg.Button("",image_filename=guardar, button_color=('White', sg.theme_background_color()), key='-GUARDAR_DATOS-'), 
         sg.Button('', image_filename=salir, button_color=('White', sg.theme_background_color()), key='-SALIR-')]
    ]

    columna_foto = [
            [sg.Text("Foto de perfil")],
            [sg.Image(filename=image_base,key='-IMAGEN-')],
            [sg.Button('', image_filename=boton_avatar, button_color=('White', sg.theme_background_color()), key="-POPUP-")]
            ]

    layout = [
        [sg.Text('Editar perfil',font=("Helvetica", 16), justification='left')],
        [sg.Column(columna_datos, element_justification='left',pad=((220, 10), 120)), sg.Column(columna_foto, element_justification='center', pad=(0,120))],
        [sg.Column(columna_botones, justification='center')]
    ]

    window = sg.Window('Editar perfil', layout,size=(900, 600))

    while True:
        evento, valores = window.read()
        
        if evento == sg.WINDOW_CLOSED:
            break

        if evento == "-POPUP-":
            popup = sg.PopupGetFile("Selecciona la imagen", initial_folder=carpeta_inicial, file_types=([("PNG Files", "*.png")]))
            if popup is not None:
                ruta_imagen = popup
                if os.path.exists(ruta_imagen):
                    nueva_ruta_imagen = redimensionar_imagen(ruta_imagen)
                    window['-IMAGEN-'].update(filename=nueva_ruta_imagen)
                    avatar = nueva_ruta_imagen
            
        if evento == "-GUARDAR_DATOS-":
            nick = valores["-NICK-"]
            nombre = valores["-NOMBRE-"]
            fecha_nacimiento = valores["-FECHA_NACIMIENTO-"]
            genero = valores["-GENERO-"]

            if not 'nueva_ruta_imagen' in locals():
                avatar = perfil["Avatar"]

            campos = campos_obligatorios(nick,nombre,fecha_nacimiento,genero)
            if campos == True:
                if nombre_valido(nombre) == True:
                    if verificar_longitud(nick, nombre, 50):
                        # Registramos el evento
                        logger.log_operation(nick, "Modifico su perfil")
                        perfil = cargar_datos(nick,nombre,fecha_nacimiento,genero,avatar)
                        sg.popup(f"Datos guardados:\nNombre: {nombre}\nNick: {nick}\nFecha de Nacimiento: {fecha_nacimiento}\nGenero: {genero}")
                    
        if evento == '-SALIR-':
            window.close()

    return perfil