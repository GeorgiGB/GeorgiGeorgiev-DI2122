# Ejercicio 11 Operaciones Linia a Linia
# Crear una aplicacion que vaya leyendo operaciones linia a linia
import os


def main():
    print("Ejercicio 11 Operaciones Linia a Linia")
    ruta_base = os.path.dirname(__file__)
    ruta_op = os.path.join(ruta_base, "op.txt")
    ruta_res = os.path.join(ruta_base, "res.txt")

    with open(ruta_op, 'r', encoding='utf-8') as f_in:
        with open(ruta_res, 'w', encoding='utf-8') as f_out:
            for linia in f_in.read().splitlines():
                parts = linia.split(" ")
                if parts[1] == '+':
                    f_out.write(str(linia + " = " + str(int(parts[0]) + int(parts[2])) + '\n'))
                elif parts[1] == '-':
                    f_out.write(str(linia + " = " + str(int(parts[0]) - int(parts[2])) + '\n'))
                elif parts[1] == '*':
                    f_out.write(str(linia + " = " + str(int(parts[0]) * int(parts[2])) + '\n'))
                elif parts[1] == '/':
                    f_out.write(str(linia + " = " + str(int(parts[0]) / int(parts[2])) + '\n'))


if __name__ == '__main__':
    main()
