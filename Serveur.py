import subprocess
import socket
import platform

a= True
def data(server_socket,conn):
    while a == True:
        try:
         data = conn.recv(1024).decode()
        except OSError:
            return ('serveur déonnecté')
        else:
            if data =='disconnect':
                reply ='disconnect'
                conn.send(reply.encode())
            else:
                print("Client : ",data)
            if data == 'kill':
                reply= 'kill'
                conn.send(reply.encode())
                conn.close()
            elif data == 'reset':
                reply='reset'
                conn.send(reply.encode())
                conn.close()
                server_socket.close()
                print('Reset du serveur')
                connect()
            else:
                if data == 'Nom':
                    reply =platform.node()
                    conn.send(reply.encode())
                if data ==' ip' or data =='ip' :
                    b=subprocess.getoutput('ipconfig  | findstr IPv4')
                    conn.send(b.encode())


def reconnect(se,conn):
    conn,address =se.accept()
    data(se,conn)
def connect():
    server_socket = socket.socket()
    server_socket.bind(('127.0.0.1', 8112))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    data(server_socket,conn)





if __name__ == '__main__':
        connect()

