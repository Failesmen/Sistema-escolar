from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QStatusBar, QAction, QVBoxLayout, QLabel, QDialog
from PyQt5.QtGui import QPixmap
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        #interface

        self.title = "Locadora de Veículos: Dor de cabeça"
        self.top = 600
        self.left = 200
        self.widht = 820
        self.height = 445
        self.setWindowIcon(QtGui.QIcon("aaaa.png"))


        self.InitWindow()


    def InitWindow(self):
        #Botao Alugar Veiculo
        self.button = QPushButton("Alugar Veículo", self)
        self.button.setIcon(QtGui.QIcon("btnAlugaVeiculo"))
        self.button.setGeometry(QtCore.QRect(10, 40, 161, 85))

        #Botao Cadastrar cliente
        self.button_2 = QPushButton("Cadastrar Cliente", self)
        self.button_2.setIcon(QtGui.QIcon("sccpre.cat-pessoa-png-1584847"))
        self.button_2.setGeometry(QtCore.QRect(170, 40, 161, 85))

        #Botao Cadastrar Veículo
        self.button_3 = QPushButton("Cadastrar Veículo", self)
        self.button_3.setIcon(QtGui.QIcon("CadastarVeiculo"))
        self.button_3.setGeometry(QtCore.QRect(330, 40, 161, 85))

        #Listar Cliente
        self.button_4 = QPushButton("Listar Cliente", self)
        self.button_4.setIcon(QtGui.QIcon("btnListVeiculo"))
        self.button_4.setGeometry(QtCore.QRect(490, 40, 161, 85))


        #Listar Alugueis
        self.button_5 = QPushButton("Listar Alugueis", self)
        self.button_5.setIcon(QtGui.QIcon("btnListAluguel"))
        self.button_5.setGeometry(QtCore.QRect(650, 40, 161, 85))

        #Imagem Veiculo
        self.label = QLabel(self)
        self.label.resize(650, 220)
        self.label.move(100, 180)
        self.label.setScaledContents(True)
        self.label.setPixmap(QtGui.QPixmap("InterfaceVeiculo"))


        mainMenu = self.menuBar()
        ArquivotitleMenu = mainMenu.addMenu("Arquivo")
        VisualizartitleMenu = mainMenu.addMenu("Visualizar")
        EditartitleMenu = mainMenu.addMenu("Editar")
        PesquisartitleMenu = mainMenu.addMenu("Pesquisar")
        AjudatitleMenu = mainMenu.addMenu("Ajuda")



        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.widht, self.height)
        self.show()
        self.statusBar().showMessage("Aluno: Failesmen Evandro | Todos os meus direitos reservados")



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())
