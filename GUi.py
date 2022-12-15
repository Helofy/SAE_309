from PyQt5.QtWidgets import *
import threading
L=[]
import csv;
f= open (r"ip.csv")
myReader = csv.reader(f)
for row in myReader:
    L.append(row)

import sys

import ClassClient

class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.Machine=ClassClient.Client('127.0.0.1',8112)
        self.i = 0
        self.setWindowTitle("QTextEdit")
        self.resize(300, 270)

        self.Host=QLabel('IP - port :')
        self.Hostip=QLineEdit()
        self.Portnum = QLineEdit()
        self.Status=QLabel('Disconnected')
        self.btnconn = QPushButton("Connexion")
        self.iplist = QComboBox()
        self.textEdit = QTextEdit()
        self.textEdit.setEnabled(False)
        self.btnPress1 = QPushButton("Add message")
        self.btnPress2 = QPushButton("Clear")
        self.message = QTextEdit()

        layout = QGridLayout()
        layout.addWidget(self.iplist, 0, 1, 1, 2)
        layout.addWidget(self.Host,1,0,1,1)
        layout.addWidget(self.Hostip,1,1,1,2)
        layout.addWidget(self.Portnum,1,2,1,1)
        layout.addWidget(self.btnconn ,1,3,1,1)
        layout.addWidget(self.Status,2,0,1,2)
        layout.addWidget(self.textEdit,3,0,2,8)
        layout.addWidget(self.btnPress1)
        layout.addWidget((self.message))
        layout.addWidget(self.btnPress2)
        for i in range (len(L)):

            self.iplist.addItem(L[i][0] +' '+ L[i][1])
        self.setLayout(layout)
        self.btnconn.clicked.connect(self.connexion)
        self.iplist.activated.connect(self.addresse)

        self.btnPress1.clicked.connect(self.btnPress1_Clicked)
        self.btnPress2.clicked.connect(self.btnPress2_Clicked)





    def addresse(self):
        IPL=self.iplist.currentText()
        IPL=IPL.split(' ')
        self.Hostip.setText(str(IPL[0]))
        self.Portnum.setText((IPL[1]))
        print(IPL[1])



    def connexion(self):
        host=str(self.Hostip.text())
        port=int(self.Portnum.text())
        self.Machine = ClassClient.Client(host,port)
        try:
            a=self.Machine.connect()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Conexion erreur")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

        else:
            if int(a) != -1:
                self.Status.setText('Connected')

            else:
                msg = QMessageBox()
                msg.setWindowTitle("Erreur")
                msg.setText('Le serveur est non lancé ou les information mauvaise !!')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()


    #        self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")

    def btnPress1_Clicked(self,Machine):

        if self.Status.text()!='Disconnected':
            text=self.message.toPlainText()
            try:

                self.textEdit.append(text)
                self.Machine.envoi(text)



            except :
                msg = QMessageBox()
                msg.setWindowTitle("Erreur")
                msg.setText("erreur message")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Le client n'est pas connecter au serveur")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()


    def btnPress2_Clicked(self):
        self.textEdit.setPlainText("")
#        self.textEdit.setHtml("<font color='red' size='6'><red>Hello PyQt5!\nHello</font>")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()
    sys.exit(app.exec_())