import collections

def string_processing():
    """
    Ingresa dos String y verifica que el primero esté contenido en el segundo
    """
    new_string = input('Ingrese un String: ')
    other_string = input('Ingrese otro String: ')
    new_string = (new_string.lower()).split()
    # Pasamos a minúsuculas para que encuentre si o si
    print(f'Palabra = {other_string}, apariciones = {new_string.count(other_string.lower())}')


string_processing()