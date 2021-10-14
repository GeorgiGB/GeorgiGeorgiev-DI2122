# Ejercicio 12 Corregir Errores del Ejercicio 11
# Modifica el codi de l’activitat 11 per a que no es produïsquen errors en l’execució, ja siga
# per introdïur valor no definits per a les funcions, valors que no són numèrics o operacions desconegudes.Controla també que no es produïsquen errors en la lectura/escriptura dels arxius.

import os


def main():
    print("Ejercicio 12 Correcciones de operaciones")

    class NoEsUnNumero(Exception):
        """Llançada quan el valor introduït no és vàlid"""
        pass

    class LongitudIncompatible(Exception):
        """Llançada quan la longitud introduida no és vàlida"""
        pass

    class SimboloIncorrecto(Exception):
        """Llançada quan el simbol introduït no és vàlid"""
        pass

    ruta_base = os.path.dirname(__file__)
    ruta_op = os.path.join(ruta_base, "op.txt")
    ruta_res = os.path.join(ruta_base, "res.txt")
    # poner UFT-8 es opcional
    with open(ruta_op, 'r', encoding='utf-8') as f_in:
        with open(ruta_res, 'w', encoding='utf-8') as f_out:
            try:
                for linea in f_in.read().splitlines():
                    parts = linea.split(" ")
                    if not len(parts) == 3:
                        raise LongitudIncompatible
                    if not parts[0].isdigit() or not parts[2].isdigit():
                        raise NoEsUnNumero
                    if parts[1] == '+':
                        f_out.write(str(linea + " = " + str(int(parts[0]) + int(parts[2])) + '\n'))
                    elif parts[1] == '-':
                        f_out.write(str(linea + " = " + str(int(parts[0]) - int(parts[2])) + '\n'))
                    elif parts[1] == '*':
                        f_out.write(str(linea + " = " + str(int(parts[0]) * int(parts[2])) + '\n'))
                    elif parts[1] == '/':
                        f_out.write(str(linea + " = " + str(int(parts[0]) / int(parts[2])) + '\n'))
                    else:
                        raise SimboloIncorrecto

            except NoEsUnNumero:
                print("Falta un numero!\n")
            except SimboloIncorrecto:
                print("Hay un simbolo incorrecto!\n")

            except LongitudIncompatible:
                print("La longitud introduida es incompatible!\n")


if __name__ == '__main__':
    main()
