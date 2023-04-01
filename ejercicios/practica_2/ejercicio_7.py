from text_7 import TEXT as text
import string

def count_letters():
    """
    Contamos la cantidad de letras mayúsculas, minúsculas y no caracteres
    """
    words = list(text)
    cant = [0,0,0]
    for item in words:
        if item in string.ascii_lowercase:
            cant[0] += 1
        elif item in string.ascii_uppercase:
            cant[1] += 1
        else:
            cant[2] += 1

    print(f'Minusculas = {cant[0]}, mayusculas = {cant[1]}, otros = {cant[2]}')

def identify_letters():
    """
    Dado un String, identifica letras mayusculas, minusculas y caracteres no letras
    Y contar las palabras totales
    """
    words = list(text)
    total_letters = set(words)
    print(f'Letras: {total_letters}')
    
def count_words():
    """
    Cuenta las palabras de un texto dado
    """
    words = text.split()
    print(f'Cantidad de palabras en el texto: {len(words)}')

identify_letters()
count_words()
count_letters()
