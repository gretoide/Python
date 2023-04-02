from text_7 import TEXT as text
import string

def count_letters():
    """
    Contamos la cantidad de letras mayúsculas, minúsculas y no caracteres
    """
    words = text.split()
    words = list(text)
    cant = {'Minusculas':0,'Mayusculas':0,'Otros':0}
    for item in words:
        if item in string.ascii_lowercase:
            cant['Minusculas'] += 1
        elif item in string.ascii_uppercase:
            cant['Mayusculas'] += 1
        else:
            cant['Otros'] += 1
    print(cant)

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
