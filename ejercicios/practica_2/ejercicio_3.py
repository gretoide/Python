from jupyter_info import JUPYTER_INFO as jupyter_text
import collections
import string

def star_with():
    """
    Verificar si la letra ingresada aparece en el texto
    """
    letter = input('Ingrese una letra: ')
    
    if (letter in string.ascii_letters):
        new_text = jupyter_text.split()
        for item in new_text:
            if item.startswith(letter):
                print(item)
    else:
        print('Error: el caracter ingresado no es una letra')
    

star_with()