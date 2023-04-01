# 8. Escriba un programa que solicite que se ingrese una palabra
# o frase y permita identificar si la misma es un Heterograma 
# (tenga en cuenta que el contenido del enlace es una traducción del inglés por 
# lo cual las palabras que nombra no son heterogramas en español). 
# Un Heterograma es una palabra o frase que no tiene 
# ninguna letra repetida entre sus caracteres.

def is_heterogram():
    """
    Nos indica si un texto es un heterograma (no tiene letras repetidas) o no
    """
    word = input('Ingrese una palabra: ')
    letters = set(word)
    if(len(word) == len(letters)):
        print(f'Es un heterograma')
    else:
        print('No es un heterograma')

is_heterogram()
