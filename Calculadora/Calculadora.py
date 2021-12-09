import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QLineEdit, QGridLayout,
                               QMainWindow, QWidget, QVBoxLayout, QPushButton)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Practica 2 Calculadora")

        # Creación del widget para su modificiación
        # y el layout al que le añadiremos los componentes
        self.widget = QWidget()
        self.layoutVBox = QVBoxLayout(self.widget)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.layoutVBox)

        # Creacion del cuadro donde saldran las operaciones
        self.operacion = QLineEdit()
        self.operacion.setReadOnly(True)
        self.layoutVBox.addWidget(self.operacion)

        # Guardar las acciones de los botones pulsados
        self.button_press = ""
        # Lista de buttons
        self.lista_buttons = {}
        # Parentesis de la calculadora
        self.parentesis_check = True
        # Layout para buttons
        button_layout = QGridLayout()

        # Listado de los caracteres que saldran en la calculadora
        caracteres = {
            '%': (0, 0), '/': (0, 1), 'x': (0, 2), '-': (0, 3, 2, 1), 'C': (0, 4),
            '7': (1, 0), '8': (1, 1), '9': (1, 2), '+': (2, 3, 2, 1), 'AC': (1, 4),
            '4': (2, 0), '5': (2, 1), '6': (2, 2), '(': (2, 4),
            '1': (3, 0), '2': (3, 1), '3': (3, 2), ')': (3, 4),
            '0': (4, 0, 1, 2), ',': (4, 2), '=': (4, 3)
        }
        # Recorremos con un for las posiciones de caracteres introducidos
        for button, pos in caracteres.items():
            self.lista_buttons[button] = QPushButton(button)
            self.lista_buttons[button].setFixedSize(60, 30)
            if len(pos) == 2:
                button_layout.addWidget(self.lista_buttons[button],
                                        pos[0], pos[1])
            else:
                # Para poder ocupar mas de una casilla se le modifica el tamaño de la misma
                # Dependiendo si queremos que sea vertical o horizontal
                if pos[3] > 1:
                    self.lista_buttons[button].setFixedSize(pos[3] * 60 + 10, 30)
                    button_layout.addWidget(self.lista_buttons[button],
                                            pos[0], pos[1], pos[2], pos[3])
                else:
                    if pos[2] > 1:
                        self.lista_buttons[button].setFixedSize(60, pos[2] * 30 + 5)
                        button_layout.addWidget(self.lista_buttons[button],
                                                pos[0], pos[1], pos[2], pos[3])
                    else:
                        self.lista_buttons[button].setFixedSize(pos[3] * 60 + 10, pos[2] * 30 + 5)
                        button_layout.addWidget(self.lista_buttons[button],
                                                pos[0], pos[1], pos[2], pos[3])

            # Seleccionamos los botones que iran en la operacion
            self.lista_buttons[button].clicked.connect(self.op)

        # Añadimos el layout con el resultado de la respuesta
        self.layoutVBox.addLayout(button_layout)
        self.lista_buttons['='].clicked.connect(self.resText)

        # Evitar fallos de diseño ya que los botones no son responsive, se arreglara mas adelante
        # Preguntar por restriccion de errores
        self.setFixedSize(350, 350)

    # Funcion donde se encontraran todas las operaciones de la calculadora
    def op(self):
        if self.sender().text() == "=":
            # Cuando el texto de QLine este vacio este no mostrara nada
            pass
        elif self.sender().text() == "C":
            self.delText()
        elif self.sender().text() == "AC":
            self.delText()
        elif self.sender().text() == "x":
            self.button_press += "*"
            self.actText(self.button_press)
        elif self.sender().text() == "()":
            if self.parentesis_check:
                self.button_press += "("
                self.parentesis_check = False
                self.actText(self.button_press)
            elif not self.parentesis_check:
                self.button_press += ")"
                self.parentesis_check = True
                self.actText(self.button_press)
        else:
            self.button_press += self.sender().text()
            # Actualización del texto al pulsar el "="
            self.actText(self.button_press)

    # Actualizar el texto
    def actText(self, text):
        self.operacion.setText(text)
        self.operacion.setFocus()

    # Borra el Texto que se muestra en la pantalla
    def delText(self):
        self.actText("")
        self.save = ""

    # Resultado de la operacion usando eval
    def resText(self):
        self.actText(str(eval(self.button_press)))


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
