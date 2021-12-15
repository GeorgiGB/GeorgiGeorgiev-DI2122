import os
import sys
from functools import partial

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QLineEdit, QGridLayout,
                               QMainWindow, QWidget, QVBoxLayout, QPushButton, QToolBar, QCheckBox)

ERROR_MSG = "NOT CORRECT"

directory = os.path.dirname(__file__)
save_res = os.path.join(directory, "res.txt")


class MainWindow(QMainWindow):
    def __init__(self, ventana1=None):
        super().__init__()
        self.setWindowTitle("Calculadora")

        # Fondo de la calculadora general
        self.setStyleSheet("background-color: #E6B0AA")

        # Creación del widget para su modificiación
        # y el layout al que le añadiremos los componentes
        self.widget = QWidget()
        self.layoutVBox = QVBoxLayout(self.widget)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.layoutVBox)

        # Menu 2

        self.ventana1 = ventana1

        # Toolbar
        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        self.addToolBar(toolbar)

        # Creacion del cuadro donde saldran las operaciones
        self.operacion = QLineEdit()
        self.operacion.setReadOnly(True)
        self.operacion.setFixedHeight(75)
        self.operacion.setStyleSheet("font: 15px; background-color: #707B7C; color: white")
        self.layoutVBox.addWidget(self.operacion)

        # Guardar las acciones de los botones pulsados
        self.button_press = ""
        # Lista de buttons
        self.lista_buttons = {}
        # Parentesis de la calculadora
        self.parentesis_check = True
        # Layout para buttons
        button_layout = QGridLayout()

        # Boton que acciona la salida de la aplicacion
        button_exit = QAction("Salir", self)
        button_exit.setShortcut("Ctrl+s")
        button_exit.setStatusTip("Con este boton sales de la calculadora")
        button_exit.triggered.connect(self.quitApp)
        self.menu = self.menuBar()
        submenu = self.menu.addMenu("&Calculadora")
        submenu.addAction(button_exit)

        # SubMenu donde se añadira el QAction para cambiar entre calculadoras
        file_submenu = submenu.addMenu("&Submenu")
        file_submenu.addAction(button_exit)
        # Añadir el QAction Quit

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
            self.lista_buttons[button].setStyleSheet("background-color: #707B7C; color: white;")
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

    def evaluate(self, operation):
        try:
            res = str(eval(operation))
        except Exception:
            res = "NOT CORRECT"
        return res

    def quitApp(self):
        self.close()

    def changeWindow(self):
        self.hide()
        if self._ventana2 is None:
            self._ventana2 = MainWindow(self)
        self._ventana2.show()

# Calculadora cientifica
class CalcCientifica(QMainWindow):
    def __init__(self, ventana2=None):
        super().__init__()

        self.setWindowTitle("Calculadora Normal")

        self.setStyleSheet("background-color: #E6B0AA;")

        # Layout General
        self.generalLayout = QVBoxLayout()

        self._ventana2 = ventana2

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Toolbar para añadir el checkbox
        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setToolButtonStyle(Qt.ToolButtonFollowStyle)
        self.addToolBar(toolbar)

        # Alterna entre "Change_Cient" y "Change_Norm" para cambiar entre las dos calculadoras
        button_action = QAction("&Change_Cient", self)
        button_action.setShortcut('Ctrl+p')
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.changeWindow)
        # Si se presiona, se sale
        button_quit = QAction("Quit", self)
        button_quit.setShortcut('Ctrl+s')
        button_quit.setStatusTip("This is your button quit")
        button_quit.triggered.connect(self.quitApp)
        # Menu
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&Calculadora")

        # SubMenu donde se añadira el QAction para cambiar entre calculadoras
        file_submenu = file_menu.addMenu("Submenu")
        file_submenu.addAction(button_action)
        # Añadir el QAction Quit
        file_menu.addAction(button_quit)

        # CheckBox, si esta True entonces al presionar "=" guardara la operacion en un .txt
        self.save_check = QCheckBox("Checkbox")
        self.save_check.setStatusTip("Checkbox")
        toolbar.addWidget(self.save_check)

        # QLineEdit
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(100)
        self.display.setStyleSheet("font: 30px; background-color: #192733; color: white")
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

        self.createButtons()
        self.connectButtons()

        caracteres = {
            '√': (0, 0), 'π': (0, 1), '**': (0, 2), 'log': (0, 3, 2, 1), 'C': (0, 4),
            '/': (1, 0), 'ln': (1, 1), 'n!': (1, 2), 'e': (1, 3),
            '7': (2, 0), '8': (2, 1), '9': (2, 2), '+': (2, 3, 2, 1), 'AC': (2, 4),
            '4': (3, 0), '5': (3, 1), '6': (3, 2), '(': (2, 4),
            '1': (4, 0), '2': (4, 1), '3': (4, 2), ')': (4, 4),
            '0': (5, 0, 1, 2), ',': (5, 2), '=': (5, 3)
        }
         # Recorremos con un for las posiciones de caracteres introducidos
        for button, pos in caracteres.items():
            self.lista_buttons[button] = QPushButton(button)
            self.lista_buttons[button].setFixedSize(60, 30)
            self.lista_buttons[button].setStyleSheet("background-color: #707B7C; color: white;")
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

        # Añadimos el layout de botones al layout principal
        self.layoutVBox.addLayout(button_layout)

        self.setFixedSize(300, 400)

    def connectButtons(self):
        # Recorre dict y utiliza la señal connect
        for text, boto in self.buttons.items():
            if text not in {"=", "C", "AC"}:
                boto.clicked.connect(partial(self.evaluateExpression, text))
        # Excepciones
        self.buttons["="].clicked.connect(self.calculateResult)
        self.display.returnPressed.connect(self.calculateResult)
        self.buttons["C"].clicked.connect(self.clearDisplay)
        self.buttons["AC"].clicked.connect(self.deleteOneChar)

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

    # Para cerrar la calculadora
    def quitApp(self):
        self.close()

    def clearDisplay(self):
        self.display.setText("")

        # Elimina carácter

    def deleteOneChar(self):
        self.display.setText(self.display.text()[:-1])

        # El boton que pulsemos se añade a la linea con el anterior

    def evaluateExpression(self, prev):
        if self.display.text() == "ERROR":
            self.clearDisplay()
        exp = self.display.text() + prev
        self.display.setText(exp)

    def saveStatus(self):
        return self.save_check.isChecked()

        # Envía el texto a la funcion evaluate y el resultado se muestra por pantalla

    def calculateResult(self):
        result = self.evaluate(self.display.text())
        total = self.display.text() + "=" + result
        self.display.setText(total)
        with open(save_res, "a") as f:
            if self.saveStatus():
                f.write(total)
                f.write("\n")

    def evaluate(self, operation):
        try:
            res = str(eval(operation))
        except Exception:
            res = "NOT CORRECT"
        return res


    def quitApp(self):
        self.close()


    def changeWindow(self):
        self.hide()
        if self._ventana2 is None:
            self._ventana2 = MainWindow(self)
        self._ventana2.show()


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
