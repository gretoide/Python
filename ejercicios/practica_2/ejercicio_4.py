from text import TEXT as text

def title():
    """
    Verificamos que el titulo tenga como máximo 10 palabras
    """
    title_list = text.split('\n')
    title_list = title_list[0].split()[1:]
    if len(title_list) <= 10:
        print('Titulo: ok')
    else:
        print('Titulo: no ok')

def summary():
    """
    Procesamos el String a partir del resumen, para controlar la lectura: 
        <= 12 - facil de leer
        13-17 - aceptable de leer
        18-25 - dificil de leer
        > 25 - muy dificil
    """
    categories = [0,0,0,0]
    sum_list = text.split('\n')
    sum_list = sum_list[1].split()[1:]
    for item in sum_list:
        if len(item) <= 12:
            categories[0] += 1
        elif len(item) <= 17:
            categories[1] += 1
        elif len(item) <= 25:
            categories[2] += 1
        else:
            categories[3] += 1

    print(f'Cantidad de oraciones fáciles de leer: {categories[0]}, aceptables para leer: {categories[1]}, dificil de leer: {categories[2]}, muy difícil de leer: {categories[3]}')

title()
summary()
