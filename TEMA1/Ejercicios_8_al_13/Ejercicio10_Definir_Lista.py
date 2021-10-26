# Ejercicio 10 Definir listas
# Definix una llista i utilitzant filter, que la separe en dues llistes, una amb els elements parells i l’altra amb els senars.


def main():
    print("Actividad 10 Definir una lista")

    # lista con los numeros
    lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # numeros pares
    pares = list(filter(lambda x: x % 2 == 0, lista))
    # numeros impares
    senars = list(filter(lambda x: x % 2 == 1, lista))

    print("Pares: ")
    for i in pares:
        print(i, end=" ,")

    print()
    print("Senars: ")
    for i in senars:
        print(i, end=" ,")


if __name__ == '__main__':
    main()
