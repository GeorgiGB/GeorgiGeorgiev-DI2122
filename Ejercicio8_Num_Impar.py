# Activitat 8 Numeros Imparells
# Fer una funcio que imprimisca els primers 100 numeros imparells


"""Funcion para devovler numeros impares"""


def main():
    cont = 0
    print("Ejercicio 8 Numeros Impares")
    for i in range(1, 300):
        if i % 2 == 1 and cont <= 100:
            print(str(cont) + ". " + str(i))
            cont += 1


if __name__ == '__main__':
    main()
