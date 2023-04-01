from readme import TEXT as text
import collections

def find():
    """
    Procesamos el String, quitando saltos de linea y espacion para luego buscar e imprimir
    las lineas que comiencen con "https" o "http"
    """
    new_text = text.split('\n')
    text_list = map(lambda item : item.strip(),new_text)
    
    for item in text_list:
        if "http" in item:
            print(item)

def max_words():
    """
    Buscamos la palabra que se encuentra la mayor cantidad de veces en el texto
    """
    new_text = text.split()
    max_word = collections.Counter(new_text).most_common()
    print(max_word)
    print(f'Mayor ocurrencia {max_word[1][0]} , {max_word[1][1]} veces')
    

find()
print('-'*30)
max_words()
