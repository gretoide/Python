import random
import json
import  clases 

archivos = ["datos1.json", "datos2.json", "datos3.json"]
ok = True


try:
    with open(random.choice(archivos), "r") as archivo:
        datos = json.load(archivo)
except FileNotFoundError:
    print('El archivo no existe')
    ok = False
except json.JSONDecodeError as Json:
    print('El archivo JSON está mal decodificado')
    ok = False


if ok:
    lista_de_usuarios = []
    for usuario in datos:
        objeto_usuario = clases.Usuario(usuario['nombre'], usuario["genero"])
        objeto_usuario.memes = usuario["memes"]
        
        lista_de_usuarios.append(objeto_usuario)

    for i in range(len(lista_de_usuarios)):
        print(lista_de_usuarios[i])

    print("FIN DEL PROGRAMA")