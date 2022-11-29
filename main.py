import subprocess
import socket
import platform

def data(conn):

    global b
    global a
    b=True

    data = conn.recv(1024).decode()

    if data =='disconnect':

        reply ='disconnect'
        conn.send(reply.encode())
        return a
    else:
        print("Client : ", data)
    if data == 'kill':

        reply= 'kill'
        conn.send(reply)
        conn.close()
        a=True
        return(a)
    if data == 'Nom':
        reply =platform.node()
        conn.send(reply.encode())

    if data =='ip':

        b=subprocess.getoutput('ipconfig  | findstr IPv4')
        conn.send(b.encode())
    else:
        reply='hello'
        conn.send(reply.encode())
if __name__ == '__main__':
    a= True
    b=True
    server_socket = socket.socket()
    server_socket.bind(('127.0.0.1', 8111))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    while a==True:

            try:
                data(conn)
            except ConnectionAbortedError:
                print("le client c'est déconnecté")
                conn, address = server_socket.accept()
            except OSError:
                print('Fermeture de la session')
                a = False



    conn.close()