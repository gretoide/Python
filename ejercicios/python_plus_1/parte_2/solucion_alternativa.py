import os
import csv

# Accedemos a la ruta donde se encuentra nuestro archivo csv
archivo = 'log_catedras.csv'
ruta_completa = os.path.abspath(os.path.join('datasets',archivo))

def usuarios_sin_entrega(ruta_completa,modo=None):
    """Retorna listado de usuarios que no vieron la "Entrega 1" """

    # Conjunto vacio para almacenar usuarios
    usuarios_vistos = set()
    usuarios_totales = set()

    # Nos guardamos los usuarios totales
    with open(ruta_completa,'r') as archivo:
        reader = csv.reader(archivo, delimiter=',')

        #Saltamos encabezado
        next(reader)

        # Agregamos todos los usuarios, y en una estructura alternativa, solo los que lo vieron
        for usuario in reader:
            nombre_usuario = usuario[1]
            contexto = usuario[3]
            evento = usuario[4]
            if "Tarea: Entrega 1" in contexto and "Se ha visualizado el estado de la entrega." in evento:
                usuarios_vistos.add(nombre_usuario)
            usuarios_totales.add(nombre_usuario)

    # Nos guardamos los usuarios que no vieron la entrega
    usuarios_sin_ver = usuarios_totales - usuarios_vistos

    # Retornamos según el modo
    if modo == 'A':
        return [usuario.upper() for usuario in usuarios_sin_ver]
    elif modo == 'a':
        return [usuario.lower() for usuario in usuarios_sin_ver]
    else:
        return usuarios_sin_ver
    

def imprimir_informacion(listado):
    """Imprime el listado de usuarios en el formato deseado"""

    print("---------------------")
    print("Usuario en el sistema")
    print("---------------------\n")
    
    for usuario in listado:
        print("-----{}-----".format(usuario))

listado_usuarios = usuarios_sin_entrega(ruta_completa)
imprimir_informacion(listado_usuarios)
