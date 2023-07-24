# Correción propia de la entrega 

import os
import csv

# Indicamos la ruta del archivo que ya se encuentra en la carpeta
archivo = "log_catedras.csv"
# Pasamos el archivo logs a otra carpeta llamada 'datasets' para tenerlo más ordenado
ruta_completa = os.path.abspath(os.path.join('datasets',archivo))

def usuarios_mas_activos(ruta_completa,orden=None):
    """Retorna un diccionario compuesto por el nombre del usuario y la cantidad de accesos"""
    with open(ruta_completa, 'r') as archivo:
        accesos = csv.reader(archivo)
        next(accesos)
    # Creamos un diccionario para almacenar la cantidad de accesos de cada usuario
        usuarios = {}

    # Recorremos la lista de accesos y actualizar el diccionario con la cantidad de accesos de cada usuario
        for nombre in accesos:
            nombre_usuario = nombre[1]
            if nombre_usuario in usuarios:
                usuarios[nombre_usuario] += 1
            else:
                usuarios[nombre_usuario] = 1

        # Ordenar el diccionario según el orden recibido, 'A' = ascendente, 'D' = descendente
        # Usamos lambda para ordenar por cantidad de accesos
        if orden == "A":
            # Convertimos a integer para no comparar con strings, ya que el csv es formato string
            usuarios_ordenados = sorted(usuarios.items(), key=lambda x: int(x[1]))
        elif orden == "D":
            usuarios_ordenados = sorted(usuarios.items(), key=lambda x: int(x[1]), reverse=True)
        else:
            usuarios_ordenados = list(usuarios.items())

        # Retornamos los 5 usuarios con más actividad 
        return usuarios_ordenados[:5]

    
def mostrar_usuarios_activos(usuarios_activos):
    """Mostramos en formato de tabla los usuarios y la cantidad de accesos"""
    # Imprimimos encabezado
    print("-" * 44)
    print("{:<25}{}".format("Usuario en el sistema", "Cantidad de accesos"))
    print("-" * 44)

    # Imprimimos usuario
    for usuario, cantidad in usuarios_activos:
        print("{:<25}{}".format(usuario, cantidad))

    print("-" * 44)

def main():
    # Creamos un menu para facilitar el manejo

    print("Seleccione una opción:")
    print("1 = Mostrar los primeros accesos")
    print("2 = Mostrar los primeros accesos de forma ASCENDENTE")
    print("3 = Mostrar los primeros accesos de forma DESCENDENTE")
    print("0 = Salir")
    
    # Menú principal
    while True:
        opcion = input("> ")
    
        if opcion == "1":
            diccionario = usuarios_mas_activos(ruta_completa)
            mostrar_usuarios_activos(diccionario)
        elif opcion == "2":
            diccionario = usuarios_mas_activos(ruta_completa, orden="A")
            mostrar_usuarios_activos(diccionario)
        elif opcion == "3":
            diccionario = usuarios_mas_activos(ruta_completa, orden="D")
            mostrar_usuarios_activos(diccionario)
        elif opcion == "0":
            print("Ha finalizado")
            break
        else:
            print("Opción inválida")

main()