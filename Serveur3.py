import subprocess
import socket
import platform,psutil
a= True
def data(server_socket,conn):
    while a == True:
        try:
         data = conn.recv(1024).decode()
        except OSError:
            return ('serveur déonnecté')


        if data =='disconnect':
                reply ='disconnect'
                conn.send(reply.encode())
        else:
            print("Client : ",data)
        c=data.split(':')
        if c[0]=='dos' and platform.platform()[:7] == 'Windows':
            try:
                awnser = subprocess.check_output(c[1],shell=True).decode('cp850').strip()
            except :
                awnser = 'commande non reconnus'
                conn.send(awnser.encode())
            else:
                if awnser =='':
                    awnser = (f'La commande {c[1]} à était exécuté')
                conn.send(awnser.encode())
        elif  c[0]== "powershell" and platform.platform()[:7] =="Windows":
            try:
                awnser = subprocess.check_output(f"powershell.exe {c[1]}", shell=True).decode('cp850').strip()
            except:
                awnser = 'commande non reconnus'
                conn.send(awnser.encode())
            else:
                conn.send(awnser.encode())
        elif data=='Linux:ls -la':

            awnser=subprocess.check_output(data,shell=True).decode('cpu850').strip()
            conn.send(awnser.encode())
        elif c[0]=='ping'and len (c[1])!=0:
            awnser=subprocess.check_output(f'ping {c[1]}',shell=True).decode('cp850').strip()
            conn.send(awnser.encode())


        elif data == 'kill':
                reply= 'Arret du serveur'
                conn.send(reply.encode())
                conn.close()
        elif data == "python --version":
            reply = subprocess.check_output(data, shell=True).decode('cp850').strip()
            conn.send(reply.encode())
        elif data == 'reset':
                reply='reset'
                conn.send(reply.encode())
                conn.close()
                server_socket.close()
                print('Reset du serveur')
                connect()

        elif data == 'Nom':
                    reply =platform.node()
                    conn.send(reply.encode())
        elif data ==' ip' or data =='ip' :
                b=subprocess.getoutput('ipconfig  | findstr IPv4')
                conn.send(b.encode())
        elif data =='os':
            b=platform.platform()[:7]
            conn.send(b.encode())
        elif data == 'ram':
            b= str(f"Pourcentage de RAM utilisée : {psutil.virtual_memory().percent}% \n RAM totale disponible {psutil.virtual_memory().total / 1024 / 1024} MB")
            conn.send(b.encode())
        elif data=='cpu':
            b=str(f" Pourcentage du cpu utilisé : {psutil.cpu_percent()}")
            conn.send(b.encode())

        else:
                conn.send('Erreur'.encode())
def reconnect(se,conn):
    conn,address =se.accept()
    data(se,conn)
def connect():
    server_socket = socket.socket()
    server_socket.bind(('192.168.10.35', 9116))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    data(server_socket,conn)
if __name__ == '__main__':
        connect()

