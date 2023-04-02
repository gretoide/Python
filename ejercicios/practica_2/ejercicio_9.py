# Escriba un programa que solicite por teclado una palabra
# y calcule el valor de la misma dada la siguiente tabla
# de valores del juego Scrabble:

def calculator():
    scrabble = ["AEIOULNRST","DG","BCMP","FHVWY","K","JX","QZ"]
    points = 0
    word = input("Juegue una palabra: ")
    word_items =list(word.upper())
    for letter in word_items:
        if letter in scrabble[0]:
            points += 1
        elif letter in scrabble[1]:
            points += 2
        elif letter in scrabble[2]:
            points +=  3
        elif letter in scrabble[3]:
            points +=  4
        elif letter in scrabble[4]:
            points +=  5
        elif letter in scrabble[5]:
            points +=  8
        else:
            points += 10
    print(f'Palabra = {word}, Puntos = {points}')

calculator()