import sys, sqlite3, time
from PyQt5 import QtGui
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QComboBox, QVBoxLayout, QGridLayout, QDialog, QWidget, QPushButton, QApplication, QMainWindow, QAction, QMessageBox, QLabel, QTextEdit, QProgressBar, QLineEdit


#B.D para as tabelas
class DBHelper():
    def __init__(self):
        self.conn = sqlite3.connect("sdms.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS students(roll INTEGER,name TEXT,gender INTEGER,branch INTEGER,year INTEGER,address TEXT,mobile INTEGER)")

        self.c.execute("CREATE TABLE IF NOT EXISTS payments(reciept_no INTEGER,roll INTEGER,fee INTEGER,semester INTEGER,reciept_date TEXT)")

        self.c.execute("CREATE TABLE IF NOT EXISTS genders(id INTEGER,name TEXT)")

        self.c.execute("CREATE TABLE IF NOT EXISTS branches(id INTEGER,name TEXT)")

    def addStudent(self,roll,name,gender,branch,year,address,mobile):

        try:
            self.c.execute("INSERT INTO students(roll,name,gender,branch,year,address,mobile) VALUES (?,?,?,?,?,?,?)" ,(roll,name,gender,branch,year,address,mobile))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(), 'Sistema Escolar', 'DADOS SALVOS COM SUCESSO!')

        except Exception:
            QMessageBox.warning(QMessageBox(), 'Sistema Escolar', 'IMPOSSIVEL SALVAR OS DADOS!')

    def searchStudent(self,roll):

        self.c.execute("SELECT * From students WHERE roll="+str(roll))
        self.data = self.c.fetchone()


        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Sistema Escolar', 'IMPOSSIVEL ENCONTRAR ALUNO DE MATRICULA: '+str(roll))
            return None

        self.list=[]
        for i in range(0,8):
            self.list.append((self.data[i]))
        self.c.close()
        self.conn.close()

        showStudent(self.list)

    def addPayment(self,roll,fee,semester):
        reciept_no=int(time.time())
        date=time.strftime("%b %d %y %H:%M:%S")

        try:
            self.c.execute("SELECT * From payments WHERE roll=" + str(roll))
            self.conn.commit()

            if not self.c.fetchone():

                if semester == 1:

                    self.c.execute("SELECT * From payments WHERE roll="+str(roll) + "AND semester=0")


                    if not self.c.fetchone():
                        QMessageBox.warning(QMessageBox(), 'Sistema Escolar',
                                            'ALUNO COM A MATRICULA Nº:' + str(roll) + 'ESTE ALUNO TEM PARCELA ATRAZADAS PARA FAZER PAGAMENTO')

                        return None

                else:
                    self.c.execute("INSERT INTO payments(reciept_no,roll,fee,semester, date) VALUES (?,?,?,?,?)",(reciept_no, roll, fee, semester, date))
                    self.conn.commit()
                QMessageBox.information(QMessageBox(), 'Sistema Escolar', 'PAGAMENTO FEITO COM SUCESSO.\nReference ID=' + str(reciept_no))

            else:


                self.c.execute("SELECT * From payments WHERE roll=" + str(roll))
                self.data = self.c.fetchall()



                if len(self.data) == 2:
                    QMessageBox.warning(QMessageBox(), 'Sistema Escolar','ALUNO COM A MATRICULA DE NUMERO: ' + str(roll) + 'JÁ FEZ O PAGAMENTO DAS DUAS PARCELAS).')



                elif semester == 1:
                    self.c.execute("SELECT * From payments WHERE roll=" +str(roll)+"AND semester=0")
                    if not self.c.fetchone():
                        QMessageBox.warning(QMessageBox(), 'Sistema Escolar', 'ALUNO COM A MATRICULA DE NUMERO: ' + str(roll) + 'TEM PARCELAS ATRASADAS.')



                    else:
                        self.c.execute("INSERT INTO payments(reciept_no,roll,fee,semester,reciept date) VALUES (?,?,?,?,?)",(reciept_no,roll,fee,semester,date))
                        self.conn.commit()
                        QMessageBox.information(QMessageBox(), 'Sistema Escolar','PAGAMENTO FEITO COM SUCESSO.\nReference ID=' + str(reciept_no))


                elif self.data[0][3] == semester:
                    QMessageBox.warning(QMessageBox(), 'Sistema Escolar', 'ALUNO COM A MATRICULA DE NUMERO: ' + str(roll) + 'JÁ PAGOU ESTE SEMESTE')


                else:
                    self.c.execute("INSERT INTO payments(reciept_no,roll,fee,semester,reciept date) VALUES (?,?,?,?,?)",(reciept_no,roll,fee,semester,date))
                    self.conn.commit()
                    QMessageBox.information(QMessageBox(), 'Sistema Escolar', 'PAGAMENTO FEITO COM SUCESSO.\nReference ID=' +str(reciept_no))


        except Exception:
            QMessageBox.warning(QMessageBox(),'Sistema Escolar', 'NÃO FOI POSSIVEL REALIZAR O PAGAMENTO')

        self.c.close()
        self.conn.close()

    def searchPayment(self,roll):
        self.c.execute("SELECT * From payments WHERE roll="+str(roll)+" ORDER BY reciept_no DESC")
        self.data = self.c.fetchone()

        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Sistema Escolar', 'IMPOSSIVEL ENCONTRAR ALUNO DE MATRICULA: '+str(roll))
            return None

        self.list = self.data
        self.c.close()
        self.conn.close()
        showPaymentFunction(self.list)


#Aba de Login do sistema
class Login(QDialog):
    def __init__(self, classe=None):
        super(Login, self).__init__(classe)
        self.setWindowIcon(QtGui.QIcon("set_of_three_books-512.png"))
        self.userNomeLabel = QLabel("Nome de Usuario")
        self.userPassLabel = QLabel("Senha de Usuario")
        self.textNome = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton("Entrar", self)
        self.buttonLogin.clicked.connect(self.FazerLogin)
        layout = QGridLayout(self)
        layout.addWidget(self.userNomeLabel, 1, 1)
        layout.addWidget(self.userPassLabel, 2, 1)

        layout.addWidget(self.textNome, 1, 2)
        layout.addWidget(self.textPass, 2, 2)
        layout.addWidget(self.buttonLogin, 3, 1, 1, 2)

        self.setWindowTitle("Login")

    def FazerLogin(self):
        if (self.textNome.text() == 'dadezpontos' and
            self.textPass.text() == 'aileleco'):
            self.accept()
        else:
            QMessageBox.warning(self, 'Sistema Escolar','DIGITAR NOME DE USUARIO E SENHA NOVAMENTE')



def showStudent(list):
        roll = 0
        gender = ""
        branch = ""
        year =""
        name = ""
        address = ""
        mobile = -1

        roll = list[0]
        name = list[1]

        if list[2] == 0:
            gender = "Masculino"
        else:
            gender = "Feminino"

        if list[3] == 0:
            branch = "Informatica"
        elif list[3] == 1:
            branch = "Química"
        elif list[3] ==2:
            branch = "Mecânica"
        elif list[3] == 3:
            branch = "Edificações"
        elif list[3] == 4:
            branch = "Eletronica"
        elif [3] == 5:
            branch = "Eletrotecnica"


        if list[4] == 0:
            year = "1 Ano"
        elif list[4] == 1:
            year = "2 Ano"
        elif list[4] == 2:
            year = "3 Ano"
        elif list[4] == 3:
            year = "4 Ano"

        mobile = list[7]
        address = list[6]

        table = QTableWidget()
        tableItem = QTableWidgetItem()
        table.setWindowTitle("Informações do Aluno")
        table.setRowCount(7)
        table.setColumnCount(2)

        table.setItem(0, 0, QTableWidgetItem("Matricula:"))
        table.setItem(0, 1, QTableWidgetItem(str(roll)))
        table.setItem(1, 0, QTableWidgetItem("Nome:"))
        table.setItem(1, 1, QTableWidgetItem(str(name)))
        table.setItem(2, 0, QTableWidgetItem("Sexo:"))
        table.setItem(2, 1, QTableWidgetItem(str(gender)))
        table.setItem(3, 0, QTableWidgetItem("Curso:"))
        table.setItem(3, 1, QTableWidgetItem(str(branch)))
        table.setItem(4, 0, QTableWidgetItem("Ano:"))
        table.setItem(4, 1, QTableWidgetItem(str(year)))
        table.setItem(5, 0, QTableWidgetItem("Endereco:"))
        table.setItem(5, 1, QTableWidgetItem(str(address)))
        table.setItem(6, 0, QTableWidgetItem("Telefone:"))
        table.setItem(6, 1, QTableWidgetItem(str(mobile)))

        table.horizontalHeader().setStretchLastSection(True)
        table.show()

        dialog = QDialog()
        dialog.setWindowTitle("Informações do Aluno")
        dialog.resize(500, 300)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec()

def showPaymentFunction(list):
        roll = -1
        recipt_no = -1
        fee = -1
        semester = -1
        recipt_date = ""

        recipt_no = list[0]
        roll = list[1]
        fee = list[2]

        if list[3] == 0:
            semester = "Semestre atrasado"
        elif list[3] == 1:
            semester = "Aluno deve pagar os semestres atrazados!"
        recipt_date = list[4]

        table = QTableWidget()
        tableItem = QTableWidgetItem()
        table.setWindowTitle("Informações de Pagamentos do Aluno")
        table.setRowCount(5)
        table.setColumnCount(2)

        table.setItem(0, 0, QTableWidgetItem("Recibo Nº:"))
        table.setItem(0, 1, QTableWidgetItem(str(recipt_no)))
        table.setItem(1, 0, QTableWidgetItem("Matricula:"))
        table.setItem(1, 1, QTableWidgetItem(str(roll)))
        table.setItem(2, 0, QTableWidgetItem("Total Taxa:"))
        table.setItem(2, 1, QTableWidgetItem(str(fee)))
        table.setItem(3, 0, QTableWidgetItem("Semestre:"))
        table.setItem(3, 1, QTableWidgetItem(str(semester)))
        table.setItem(4, 0, QTableWidgetItem("Data Pagamento:"))
        table.setItem(4, 1, QTableWidgetItem(str(recipt_date)))
        table.horizontalHeader().setStretchLastSection(True)
        table.show()
        dialog = QDialog()
        dialog.setWindowTitle("Informações de Pagamentos")
        dialog.resize(500, 300)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec()


class AddStudent(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("set_of_three_books-512.png"))
        self.gender = -1
        self.branch = -1
        self.year = -1
        self.roll = -1
        self.name = ""
        self.address = ""
        self.mobile = -1

        self.btnCancel = QPushButton("Cancelar", self)
        self.btnAtualizar = QPushButton("Atualizar", self)
        self.btnAdd = QPushButton("Adicionar", self)

        self.btnCancel.setFixedHeight(30)
        self.btnAtualizar.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.yearCombo = QComboBox(self)
        self.yearCombo.addItem("1")
        self.yearCombo.addItem("2")
        self.yearCombo.addItem("3")
        self.yearCombo.addItem("4")

        self.genderCombo = QComboBox(self)
        self.genderCombo.addItem("Masculino")
        self.genderCombo.addItem("Feminino")

        self.branchCombo = QComboBox(self)
        self.branchCombo.addItem("Informatica")
        self.branchCombo.addItem("Química")
        self.branchCombo.addItem("Mecânica")
        self.branchCombo.addItem("Edificações")
        self.branchCombo.addItem("Eletronica")
        self.branchCombo.addItem("Eletrotecnica")


        self.rollLabel = QLabel("Matricula Nº")
        self.nameLabel = QLabel("Nome")
        self.addressLabel = QLabel("Endereço")
        self.mobileLabel = QLabel("Telefone")
        self.yearLabel = QLabel("Ano Atual")
        self.branchLabel = QLabel("Curso")
        self.genderLabel = QLabel("Sexo")

        self.rollText = QLineEdit(self)
        self.nameText = QLineEdit(self)
        self.addressText = QLineEdit(self)
        self.mobileText = QLineEdit(self)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.rollLabel, 1, 1)
        self.grid.addWidget(self.nameLabel, 2, 1)
        self.grid.addWidget(self.genderLabel, 3, 1)
        self.grid.addWidget(self.addressLabel, 4, 1)
        self.grid.addWidget(self.mobileLabel, 5, 1)
        self.grid.addWidget(self.branchLabel, 6, 1)
        self.grid.addWidget(self.yearLabel, 7, 1)

        self.grid.addWidget(self.rollText, 1, 2)
        self.grid.addWidget(self.nameText, 2, 2)
        self.grid.addWidget(self.genderCombo, 3, 2)
        self.grid.addWidget(self.addressText, 4, 2)
        self.grid.addWidget(self.mobileText, 5, 2)
        self.grid.addWidget(self.branchCombo, 6, 2)
        self.grid.addWidget(self.yearCombo, 7, 2)

        self.grid.addWidget(self.btnAtualizar, 9, 1)
        self.grid.addWidget(self.btnCancel, 9, 3)
        self.grid.addWidget(self.btnAdd, 9, 2)

        self.btnAdd.clicked.connect(self.addStudent)
        self.btnCancel.clicked.connect(QApplication.instance().quit)
        self.btnAtualizar.clicked.connect(self.formatar)

        self.setLayout(self.grid)
        self.setWindowTitle("Sistema Escolar: Cadastrar Aluno")
        self.resize(500, 300)
        self.show()
        self.exec()

    def formatar(self):
        self.rollText.setText("")
        self.nameText.setText("")
        self.addressText.setText("")
        self.mobileText.setText("")

    def addStudent(self):
        self.gender = self.genderCombo.currentIndex()
        self.year = self.yearCombo.currentIndex()
        self.branch = self.branchCombo.currentIndex()
        self.roll = int(self.rollText.text())
        self.name = self.nameText.text()
        self.address = self.addressText.text()
        self.mobile = self.mobileText.text()

        self.dbhelper=DBHelper()
        self.dbhelper.addStudent(self.roll, self.name, self.gender, self.branch,
                                 self.year, self.address, self.mobile)

class AddPayment(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("set_of_three_books-512.png"))
        self.reciept_no = -1
        self.roll = -1
        self.fee = -1
        self.semester = -1
        self.data = -1

        self.btnCancel = QPushButton("Cancelar", self)
        self.btnAtualizar = QPushButton("Atualizar", self)
        self.btnAdd = QPushButton("Adicionar", self)

        self.btnCancel.setFixedHeight(30)
        self.btnAtualizar.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.semesterCombo = QComboBox(self)
        self.semesterCombo.addItem("Primeiro")
        self.semesterCombo.addItem("Segundo")

        self.rollLabel = QLabel("Matricula Nº")
        self.feeLabel = QLabel("Total Taxa")
        self.semesterLabel = QLabel("Semestre:")

        self.rollText = QLineEdit(self)
        self.feeLabelText= QLineEdit(self)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.rollLabel, 1, 1)
        self.grid.addWidget(self.feeLabel, 2, 1)
        self.grid.addWidget(self.semesterLabel, 3, 1)

        self.grid.addWidget(self.rollText, 1, 2)
        self.grid.addWidget(self.feeLabelText, 2, 2)
        self.grid.addWidget(self.semesterCombo, 3, 2)

        self.grid.addWidget(self.btnAtualizar, 4, 1)
        self.grid.addWidget(self.btnCancel, 4, 3)
        self.grid.addWidget(self.btnAdd, 4, 2)

        self.btnAdd.clicked.connect(self.addPayment)
        self.btnCancel.clicked.connect(QApplication.instance().quit)
        self.btnAtualizar.clicked.connect(self.reset)

        self.setLayout(self.grid)
        self.setWindowTitle("Sistema Escolar:Adicionar Pagamento")
        self.resize(400, 200)
        self.show()
        self.exec()

    def reset(self):
        self.rollText.setText("")
        self.feeLabelText.setText("")

    def addPayment(self):
        self.semester = self.semesterCombo.currentIndex()
        self.roll = int(self.rollText.text())
        self.fee = int(self.feeLabelText.text())

        self.dbhelper = DBHelper()
        self.dbhelper.addPayment(self.roll, self.fee, self.semester)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusBar().showMessage("Aluno: Failesmen Evandro | Todos os meus direitos reservados")

        self.setWindowIcon(QtGui.QIcon("set_of_three_books-512.png"))

        self.rollToBeSearched = 0
        self.vbox = QVBoxLayout()
        self.text = QLabel("Numero da Matricula Aluno :")
        self.editField = QLineEdit()
        self.btnSearch = QPushButton("Pesquisar", self)
        self.btnSearch.clicked.connect(self.showStudent)
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.editField)
        self.vbox.addWidget(self.btnSearch)
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Numero Matricula:")
        self.dialog.setLayout(self.vbox)

        self.rollForPayment = 0
        self.vboxPayment = QVBoxLayout()
        self.textPayment = QLabel("Matricula numero:")
        self.editFieldPayment = QLineEdit()
        self.btnSearchPayment = QPushButton("Pesquisar", self)
        self.btnSearchPayment.clicked.connect(self.showStudentPayment)
        self.vboxPayment.addWidget(self.textPayment)
        self.vboxPayment.addWidget(self.editFieldPayment)
        self.vboxPayment.addWidget(self.btnSearchPayment)
        self.dialogPayment = QDialog()
        self.dialogPayment.setWindowTitle("NUMERO DE MATRICULA:")
        self.dialogPayment.setLayout(self.vboxPayment)

        self.btnEnterStudent = QPushButton("Cadastrar Aluno", self)
        self.btnEnterPayment = QPushButton("Cadastrar Pagamentos", self)
        self.btnShowStudentDetails = QPushButton("Listar Aluno", self)
        self.btnShowPaymentDetails = QPushButton("Listar Pagamento", self)

        self.picLabel = QLabel(self)
        self.picLabel.resize(240, 200)
        self.picLabel.move(170, 100)
        self.picLabel.setScaledContents(True)
        self.picLabel.setPixmap(QtGui.QPixmap("LogoPrincipal.png"))

        self.btnEnterStudent.move(0, 25)
        self.btnEnterStudent.resize(140, 60)
        self.btnEnterStudent.setIcon(QtGui.QIcon("alunoicone"))
        self.btnEnterStudentFont = self.btnEnterStudent.font()
        self.btnEnterStudentFont.setPointSize(8)
        self.btnEnterStudent.setFont(self.btnEnterStudentFont)
        self.btnEnterStudent.clicked.connect(self.enterstudent)

        self.btnEnterPayment.move(140, 25)
        self.btnEnterPayment.resize(140, 60)
        self.btnEnterPayment.setIcon(QtGui.QIcon("pagamentoicone"))
        self.btnEnterPaymentFont = self.btnEnterStudent.font()
        self.btnEnterPaymentFont.setPointSize(7)
        self.btnEnterPayment.setFont(self.btnEnterPaymentFont)
        self.btnEnterPayment.clicked.connect(self.enterpayment)

        self.btnShowStudentDetails.move(280, 25)
        self.btnShowStudentDetails.resize(140, 60)
        self.btnShowStudentDetails.setIcon(QtGui.QIcon("listaaluno"))
        self.btnShowStudentDetailsFont = self.btnEnterStudent.font()
        self.btnShowStudentDetailsFont.setPointSize(8)
        self.btnShowStudentDetails.setFont(self.btnShowStudentDetailsFont)
        self.btnShowStudentDetails.clicked.connect(self.showStudentDialog)

        self.btnShowPaymentDetails.move(420, 25)
        self.btnShowPaymentDetails.resize(140, 60)
        self.btnShowPaymentDetails.setIcon(QtGui.QIcon("listapagamento"))
        self.btnShowPaymentDetailsFont = self.btnEnterStudent.font()
        self.btnShowStudentDetailsFont.setPointSize(8)
        self.btnShowPaymentDetails.setFont(self.btnShowStudentDetailsFont)
        self.btnShowPaymentDetails.clicked.connect(self.showStudentPaymentDialog)

        #Menu do coisa lá
        mainMenu = self.menuBar()
        ArquivotitleMenu = mainMenu.addMenu("Arquivo")
        VisualizartitleMenu = mainMenu.addMenu("Visualizar")
        EditartitleMenu = mainMenu.addMenu("Editar")
        PesquisartitleMenu = mainMenu.addMenu("Pesquisar")
        AjudatitleMenu = mainMenu.addMenu("Ajuda")

        self.resize(560, 350)
        self.setWindowTitle("Sistema Escolar: Hogwarts")

    def enterstudent(self):
        enterStudent=AddStudent()
    def enterpayment(self):
        enterpayment=AddPayment()
    def showStudentDialog(self):
        self.dialog.exec()
    def showStudentPaymentDialog(self):
        self.dialogPayment.exec()
    def showStudent(self):
        if self.editField.text() is "":
            QMessageBox.warning(QMessageBox(), 'Sistema Escolar', 'DIGITE O NUMERO DA MATRICULA PARA O RESULTADO')
            return None

        showstudent = DBHelper()
        showstudent.searchStudent(int(self.editField.text()))
    def showStudentPayment(self):
        if self.editFieldPayment.text() is "":
            QMessageBox.warning(QMessageBox(), 'Sistema Escolar', 'POR FAVOR, DIGITAR O NUMERO DA MATRICULA')

            return None
        showstudent = DBHelper()
        showstudent.searchPayment(int(self.editFieldPayment.text()))

if __name__ == '__main__':
    App = QApplication(sys.argv)
    login = Login()

    if login.exec() == QDialog.Accepted:
        window = Window()
        window.show()
    sys.exit(App.exec())









