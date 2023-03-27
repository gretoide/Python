from random import choice, randrange
from datetime import datetime
# Operadores posibles
operators = ["+", "-", "*", "/"]
# Cantidad de cuentas a resolver
times = 5
# Contador inicial de tiempo.
# Esto toma la fecha y hora actual.
init_time = datetime.now()
print(f"¡Veremos cuanto tardas en responder estas {times} operaciones!")
right = 0
for i in range(0, times):
    # Se eligen números y operador al azar
    number_1 = randrange(10)
    number_2 = randrange(10)
    operator = choice(operators)
    if(operator == "/")and(number_2 == 0):
<<<<<<< HEAD
        print("No")
=======
<<<<<<< HEAD
        print("No se puede calcular por cero, se calculará un nuevo número.")
=======
        print("No")
>>>>>>> d2ffa7850177c4bb68ffbb947053adce6dd4a02f
>>>>>>> 2a25ade (Update)
        number_2 = randrange(1,10)
    match operator:
        case "+":
                operation = number_1 + number_2
        case "-":
                operation = number_1 - number_2
        case "/":
                operation = number_1 / number_2
        case "*":
                operation = number_1 * number_2
    # Se imprime la cuenta.
    print(f"{i+1}- ¿Cuánto es {number_1} {operator} {number_2}?")
    # Le pedimos al usuario el resultado
    result = float(input("resultado: "))
    # Mostramos por pantalla si el resultado es correcto o no
    if (result == operation):
        print("correcto!")
        right += 1
    else:
        print("incorrecto")
    # Al terminar toda la cantidad de cuentas por resolver.
    # Se vuelve a tomar la fecha y la hora.
    end_time = datetime.now()
    # Restando las fechas obtenemos el tiempo transcurrido.
    total_time = end_time - init_time
    # Mostramos ese tiempo en segundos.
    print(f"\n Tardaste {total_time.seconds} segundos.")
print(f"intentos correctos: {right}")
print(f"intentos fallidos: {times - right}")