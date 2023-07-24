import PySimpleGUI as sg
import os
import json
import re
from ...paths import RUTA_BASE , DATABASE, IMAGENES, FOTOS_DE_PERFIL, ICONOS, BOTONES
from ...log.src import event_log

icono_calendario = os.path.join(ICONOS,'calendario.png')
imagen_inicial= os.path.join(FOTOS_DE_PERFIL,'avatar_predeterminado.png')
carpeta_inicial = os.path.join(IMAGENES,'fotos_de_perfil')
json_file = os.path.join(DATABASE,'datos.json')

guardar = os.path.join(BOTONES,"button_guardar.png")
boton_avatar = os.path.join(BOTONES,"button_agregar-avatar.png")
salir = os.path.join(BOTONES,"button_salir.png")

opciones = ['Femenino','Masculino','Otro']

datos_nuevo_usuario = []

def obtener_ruta_imagen(inicial):
    """Obtiene la ruta de la imagen correspondiente a la inicial del nick"""
    inicial = inicial.lower()
    ruta_imagen = os.path.join(FOTOS_DE_PERFIL, f"letter-{inicial}.png")
    if os.path.exists(ruta_imagen):
        return ruta_imagen
    else:
        return imagen_inicial

def verificar_archivo():
    """Verificar si el archivo JSON existe"""
    if not os.path.exists(json_file):
        with open(json_file, "w") as archivo_json:
            json.dump([], archivo_json)
        return open(json_file, "r+")
    else:
        return open(json_file, "r+")

def agregar_usuario(nick, nombre, fecha_nacimiento, sexo, avatar):
    """Agregar un usuario al archivo JSON"""
    nuevo_usuario = {
        "Alias": nick,
        "Nombre": nombre,
        "Fecha de nacimiento": fecha_nacimiento,
        "Sexo": sexo,
        "Avatar": avatar
    }
    
    with verificar_archivo() as archivo:
        datos = json.load(archivo)
        
        # Obtenemos la lista de usuarios directamente del archivo
        lista_usuarios = datos
        
        # Agregamos el nuevo usuario a la lista
        lista_usuarios.append(nuevo_usuario)
        
        archivo.seek(0)  # Regresamos al inicio del archivo
        json.dump(lista_usuarios, archivo, indent=4)  # Guardamos la lista actualizada en el archivo

def es_igual(nick, nombre, fecha_nacimiento, sexo, avatar):
    """ 
    Verifica si el nick ingresado ya existe en el archivo JSON.
    """
    # Abrir el archivo JSON y cargar los datos en una lista de diccionarios
    with open(json_file, "r") as archivo:
        datos = json.load(archivo)
    
    # Verificar si algún diccionario en la lista tiene una clave "Alias" igual al nick ingresado
    if any(diccionario["Alias"].lower() == nick.lower() for diccionario in datos):
        sg.popup(f"El alias '{nick}' ya existe!")
        return False
    else:
        agregar_usuario(nick, nombre, fecha_nacimiento, sexo, avatar)
        sg.popup(f"Usuario '{nick}' agregado correctamente.")
        return True

def campos_obligatorios(nick, nombre, fecha_nacimiento, sexo):
    """
    Verifica si los campos obligatorios están completos.
    """
    if nick == "" or nombre == "" or fecha_nacimiento == "" or (sexo == "" or sexo == "Seleccione genero"):
        sg.popup("Debe completar todos los campos")
        return False
    else:
        return True

def nombre_valido(nombre):
    """Verifica si el nombre contiene solamente letras del abecedario"""
    patron = r'^[a-zA-Z]+$'
    if re.match(patron, nombre) is None:
        sg.Popup('Error', 'El nombre contiene caracteres no permitidos')
        return False
    return True

def verificar_longitud(nick, nombre, max_caracteres):
    """Verifica si el nick y el nombre tienen una longitud menor o igual a max_caracteres"""
    if len(nick) > max_caracteres:
        sg.popup(f"El nick debe tener como máximo {max_caracteres} caracteres")
        return False
    elif len(nombre) > max_caracteres:
        sg.popup(f"El nombre debe tener como máximo {max_caracteres} caracteres")
        return False
    return True

def main_nuevo_perfil():
    """
    Abre la ventana para crear un nuevo perfil.

    - Muestra una ventana con campos para ingresar los datos del nuevo perfil.
    - Permite al usuario completar los campos de nick, nombre, fecha de nacimiento y género.
    - Verifica si todos los campos obligatorios están completos antes de guardar los datos.
    - Verifica la longitud del nick y el nombre.
    - Si los campos están completos y cumplen con la longitud, guarda los datos del nuevo perfil y muestra un mensaje emergente con la información guardada.
    - Registra el evento de registro del nuevo perfil en el registro de eventos.
    - Cierra la ventana después de guardar los datos o al cerrar la ventana.
    """
    logger = event_log.EventLogger()

    columna_datos = [
        [sg.Text("Nick:", justification='right', size=(15, 1)), sg.Input(key="-NICK-", size=(30, 1))],
        [sg.Text("Nombre:", justification='right', size=(15, 1)), sg.Input(key="-NOMBRE-", size=(30, 1))],
        [sg.Text("Fecha de nacimiento:", justification='right', size=(18, 1)), sg.InputText(key="-FECHA_NACIMIENTO-", disabled=True, text_color=('Black'), size=(25, 1), pad=(10, 0)),
        sg.CalendarButton('', image_filename=icono_calendario, target="-FECHA_NACIMIENTO-", format='%Y-%m-%d', button_color=('LightGrey', sg.theme_background_color()))],
        [sg.Text("Género:", justification='right', size=(15, 1)), sg.Combo(opciones, default_value='Seleccione genero', size=(30, 1), key='-GENERO-', readonly=True)],
    ]

    columna_botones = [
        [sg.Button("", image_filename=guardar, button_color=('White', sg.theme_background_color()), key='-GUARDAR_DATOS-'), 
         sg.Button('', image_filename=salir, button_color=('White', sg.theme_background_color()), key='-SALIR-')]
    ]

    layout = [
        [sg.Text('Nuevo perfil', font=("Helvetica", 16), justification='left')],
        [sg.Column(columna_datos, element_justification='center',  pad=(200, 120))],
        [sg.Column(columna_botones, justification='center', element_justification='center')]
    ]

    window = sg.Window('Nuevo perfil', layout, size=(900, 600))

    while True:
        ima_path = imagen_inicial
        JSON = verificar_archivo()
        evento, valores = window.read()

        if evento == sg.WINDOW_CLOSED:
            window.close()
            break
         
        if evento == '-SALIR-':
            break
        
        if evento == "-GUARDAR_DATOS-":
            nick = valores["-NICK-"]
            nombre = valores["-NOMBRE-"]
            fecha_nacimiento = valores["-FECHA_NACIMIENTO-"]
            genero = valores["-GENERO-"]
            campos = campos_obligatorios(nick, nombre, fecha_nacimiento, genero)
            if campos:
                if verificar_longitud(nick, nombre, 30):  # Verificar que el nick y el nombre tengan una longitud menor o igual al parametro
                    ruta_imagen = obtener_ruta_imagen(nick[0])
                    avatar = os.path.relpath(ruta_imagen, FOTOS_DE_PERFIL)
                    if nombre_valido(nombre):
                        try: 
                            agregado = es_igual(nick, nombre, fecha_nacimiento, genero, avatar)
                        except UnboundLocalError:
                            avatar = imagen_inicial
                            agregado = es_igual(nick, nombre, fecha_nacimiento, genero, avatar)
                        if agregado:
                            # Registramos el evento
                            logger.log_operation(nick, "Se registro en la app")
                            sg.popup(f"Datos guardados:\nNombre: {nombre}\nNick: {nick}\nFecha de Nacimiento: {fecha_nacimiento}\nGenero: {genero}")
                            window.close()
    window.close()

