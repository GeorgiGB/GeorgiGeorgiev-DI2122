import os
import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QLineEdit, QGridLayout,
                               QMainWindow, QSizePolicy, QWidget, QVBoxLayout, QPushButton,
                               QStackedLayout, QStatusBar, QLabel)

ERROR_MSG = "NOT CORRECT"

directory = os.path.dirname(__file__)
save_res = os.path.join(directory, "res.txt")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora")

        # Fondo de la calculadora general
        self.setStyleSheet("background-color: none")

        # Creación del menu principal que mostrara el programa
        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # Menu 1 normal
        self.calcPrincipal = QWidget()
        self.layoutPrincipal = QVBoxLayout(self.calcPrincipal)
        self.calcPrincipal.setLayout(self.layoutPrincipal)

        # Menu 2 cientifica
        self.calcCientifica = QWidget()
        self.layoutCientifica = QVBoxLayout(self.calcCientifica)
        self.calcCientifica.setLayout(self.layoutCientifica)

        # Con el StackedLayout podremos acceder a los dos tipos de calculadoras
        self.stackedLayout = QStackedLayout(self.widget)
        self.stackedLayout.addWidget(self.calcPrincipal)
        self.stackedLayout.addWidget(self.calcCientifica)

        self.stackedLayout.setCurrentWidget(self.calcPrincipal)

        # QAction para cerrar aplicacion
        buttonExit = QAction("Quit", self)
        buttonExit.setShortcut('Ctrl+q')
        buttonExit.setStatusTip("Salir")
        buttonExit.triggered.connect(self.quitApp)

        # QAction para cambiar a la calculadora Principal
        buttonPrincipal = QAction("&Normal", self)
        buttonPrincipal.setShortcut('Ctrl+p')
        buttonPrincipal.setStatusTip("Calculadora Normal")
        buttonPrincipal.triggered.connect(self.modoPrincipal)

        # QAction para cambiar a la calculadora Cientifica
        buttonCientifica = QAction("&Cientifica", self)
        buttonCientifica.setShortcut('Ctrl+c')
        buttonCientifica.setStatusTip("Calculadora Cientifica")
        buttonCientifica.triggered.connect(self.modoCientifico)

        # Creacion del cuadro donde saldran las operaciones
        self.operacion = QLineEdit()
        self.operacion.setReadOnly(True)
        self.operacion.setFixedHeight(75)
        self.operacion.setStyleSheet("font: 15px; background-color: #707B7C; color: white")
        self.layoutPrincipal.addWidget(self.operacion)

        #Status Bar
        self.setStatusBar((QStatusBar(self)))
        self.cambiarCalc = QLabel("Calculadora Normal")
        self.cambiarCalc.setScaledContents(True)
        self.statusBar().addPermanentWidget(self.cambiarCalc)
        self.statusBar().addPermanentWidget(QLabel("|"))

        # SubMenu donde se añadira el QAction para cambiar entre calculadoras
        self.menu = self.menuBar()
        submenu = self.menu.addMenu("&Menu")
        submenu.addAction(buttonPrincipal)
        submenu.addAction(buttonCientifica)

        # Y aqui estan los botones que saldran en el submenu
        categoriaSubmenu = submenu.addMenu("&Submenu")
        categoriaSubmenu.addAction(buttonPrincipal)
        categoriaSubmenu.addAction(buttonCientifica)
        categoriaSubmenu.addAction(buttonExit)

        # Guardar las acciones de los botones pulsados
        self.button_press = ""
        # Lista de buttons
        self.caractNormal = []
        # Parentesis de la calculadora
        self.parentesis_check = True
        # Layout para buttons
        button_layout = QGridLayout()

        # Apartado de la calculadora principal
        self.ventanaPrincipal = QLineEdit()
        self.ventanaPrincipal.setAlignment(Qt.AlignLeft)
        self.ventanaPrincipal.setFixedHeight(75)
        self.ventanaPrincipal.setReadOnly(True)
        self.layoutPrincipal.addWidget(self.ventanaPrincipal)

        # Listado de los caracteres que saldran en la calculadora
        caractNormal = {
            '%': (0, 0, 1, 1), '/': (0, 1, 1, 1), 'x': (0, 2, 1, 1), '<-': (0, 3, 2, 1), 'C': (0, 4, 1, 1),
            'e': (1, 0, 1, 1), 'ln': (1, 1, 1, 1), 'n!': (1, 2, 1, 1), '-': (1, 3, 1, 1),
            '7': (1, 0, 1, 1), '8': (1, 1, 1, 1), '9': (2, 2, 1, 1), '+': (2, 3, 2, 1), 'AC': (1, 4, 1, 1),
            '4': (2, 0, 1, 1), '5': (2, 1, 1, 1), '6': (3, 2, 1, 1), '(': (2, 4, 1, 1),
            '1': (3, 0, 1, 1), '2': (3, 1, 1, 1), '3': (4, 2, 1, 1), ')': (3, 4, 1, 1),
            '0': (5, 0, 1, 2), ',': (5, 2, 1, 1), '=': (5, 3, 1, 2)
        }

        # Recorremos con un for las posiciones de caracteres introducidos
        for key in caractNormal.keys():
            button = QPushButton(key)
            self.caractNormal.append(button)
            button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            button.setStyleSheet("background-color: #707B7C; color: white;")
            button_layout.addWidget(button, caractNormal[key][0], caractNormal[key][1],
                                    caractNormal[key][2], caractNormal[key][3])

            # Seleccionamos los botones que iran en la operacion
            button.clicked.connect(self.op)

        # Apartado de calculadora cientifica
        self.ventanaCientifica = QLineEdit()
        self.ventanaCientifica.setAlignment(Qt.AlignLeft)
        self.ventanaCientifica.setFixedHeight(75)
        self.ventanaCientifica.setReadOnly(True)
        self.layoutCientifica.addWidget(self.ventanaCientifica)

        self.caractCientifica = []

        caractCientifica = {
            '√': (0, 0, 1, 1), 'π': (0, 1, 1, 1), '**': (0, 2, 1, 1), 'log': (0, 3, 2, 1), 'C': (0, 4, 1, 1),
            '/': (1, 0, 1, 1), 'ln': (1, 1, 1, 1), 'n!': (1, 2, 1, 1), 'e': (1, 3, 1, 1),
            '7': (2, 0, 1, 1), '8': (2, 1, 1, 1), '9': (2, 2, 1, 1), '+': (2, 3, 2, 1), 'AC': (1, 4, 1, 1),
            '4': (3, 0, 1, 1), '5': (3, 1, 1, 1), '6': (3, 2, 1, 1), '(': (2, 4, 1, 1),
            '1': (4, 0, 1, 1), '2': (4, 1, 1, 1), '3': (4, 2, 1, 1), ')': (3, 4, 1, 1),
            '0': (5, 0, 1, 2), ',': (5, 2, 1, 1), '=': (5, 3, 1, 2)
        }

        for key in caractCientifica.keys():
            button = QPushButton(key)
            self.caractCientifica.append(button)
            button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
            button.setStyleSheet("background-color: #707B7C; color: white;")
            button_layout.addWidget(button, caractCientifica[key][0], caractCientifica[key][1],
                                    caractCientifica[key][2], caractCientifica[key][3])

            # Seleccionamos los botones que iran en la operacion
            button.clicked.connect(self.op)

        # Evitar fallos de diseño ya que los botones no son responsive, se arreglara mas adelante
        # Preguntar por restriccion de errores
        # Añadimos el layout con el resultado de la respuesta
        self.layoutPrincipal.addLayout(button_layout)
        self.setFixedSize(360, 360)

    # Funcion donde se encontraran todas las operaciones de la calculadora
    def op(self):
        if self.sender().text() == "=":
            # Cuando el texto de QLine este vacio este no mostrara nada
            self.actText(str(eval(self.button_press)))
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

    # Cambia al modo basico
    def modoPrincipal(self):
        self.stackedLayout.setCurrentWidget(self.calcPrincipal)
        self.cambiarCalc.setText("Calculadora Principal")

    # Cambia a modo cientifico
    def modoCientifico(self):
        self.stackedLayout.setCurrentWidget(self.calcCientifica)
        self.cambiarCalc.setText("Calculadora Cientifica")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
