from PyQt5.QtWidgets import *
import os,pathlib
from PyQt5.QtCore import *
import csv
L=[]
import sys
import ClassClient
class App(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cont=0
        self.fichier='ip.csv'
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
        self.btnquit=QPushButton('Quit')
        self.btnquit.hide()
        self.btnnewwin=QPushButton('New Connexion')
        self.addconn=QPushButton('Ajouter au fichier')

        self.lirefich=QPushButton("Lire un fichier CSV")
        self.btnPress1 = QPushButton("Add message")
        self.btnPress2 = QPushButton("Clear")
        self.message = QTextEdit()
        layout = QGridLayout()
        layout.addWidget(self.iplist, 0, 1, 1, 2)
        layout.addWidget(self.lirefich,0,0,1,1)
        layout.addWidget(self.Host,1,0,1,1)
        layout.addWidget(self.Hostip,1,1,1,2)
        layout.addWidget(self.Portnum,1,2,1,1)
        layout.addWidget(self.btnconn ,1,3,1,1)
        layout.addWidget(self.Status,2,0,1,2)
        layout.addWidget(self.btnquit,2,2,1,1)
        layout.addWidget(self.addconn,1,4,1,1)
        layout.addWidget(self.btnnewwin,0,3,1,1)

        layout.addWidget(self.textEdit,3,0,2,8)
        layout.addWidget(self.btnPress1)
        layout.addWidget((self.message))
        layout.addWidget(self.btnPress2)
        self.setLayout(layout)
        self.addconn.clicked.connect(self.addfich)
        self.btnnewwin.clicked.connect(self.newwindos)
        self.btnconn.clicked.connect(self.connexion)
        self.iplist.activated.connect(self.addresse)
        self.lirefich.clicked.connect(self.ouvrir)
        self.btnPress1.clicked.connect(self.envoiemess)
        self.btnPress2.clicked.connect(self.clear)
        self.btnquit.clicked.connect(self.quit)
    def ouvrir(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "Choisissez votre fichier", "", "Fichiers csv (*.csv)", options=options)
            fichier = pathlib.Path(fileName).name
            file = open(f"{fichier}", 'r')
            myReader = csv.reader(file)
            for row in myReader:
                L.append(row)
            for i in range (len(L)):
                self.iplist.addItem(L[i][0] +' '+ L[i][1])
        except :
            msg = QMessageBox()
            msg.setWindowTitle("Attention")
            msg.setText("Vous n'avez pas séléctionner de fichier")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            self.fichier=fichier
    def addresse(self):
        IPL = self.iplist.currentText()
        IPL = IPL.split(' ')
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
                self.btnquit.show()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Erreur")
                msg.setText('Le serveur est non lancé ou les information mauvaise !!')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
    def envoiemess(self,Machine):
        if self.Status.text()!='Disconnected':
            text=self.message.toPlainText()
            if text =='':
                msg = QMessageBox()
                msg.setWindowTitle("Erreur")
                msg.setText("le message est vide !!")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
            else:
                self.textEdit.append(text)
                try:
                    awnser=self.Machine.dialogue(text)
                    if str(awnser) == 'Erreur':
                        msg = QMessageBox()
                        msg.setWindowTitle("Erreur")
                        msg.setText("le serveur n'as rien retourner ")
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                    else:
                        self.textEdit.append(f"{awnser}\n")
                    self.message.clear()
                except:
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
    def clear(self):
        self.textEdit.setPlainText("")
    def quit(self):
        self.Machine.dialogue('kill')
        QCoreApplication.exit(0)
    def newwindos(self):
        self.win=App()
        self.win.show()
    def addfich(self):

        file=open(self.fichier,'a')

        ip=self.Hostip.text()
        port=self.Portnum.text()
        if len(ip)!=0:
            if self.cont ==0:
                file.write('\n'+ip +','+port)
            else:
                file.write( '\n'+ip + ',' + port )
            self.cont+=1
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("l'ip n'est pas valide")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        file.close()

        self.iplist.addItem(ip +' '+port)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())