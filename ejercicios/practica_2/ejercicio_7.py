from text_7 import TEXT as text
import string

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
