import socket
def data():
    global a
    message = input("Client : ")
    if message == "disconnect":
        client_socket.send('disconnect'.encode())
        client_socket.close()
        a=False
        return (a)
    else:
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        if data != "":
            if data == "disconnect":
                print("Serveur : ", data)
                client_socket.send('disconnect'.encode())
                client_socket.close()
                a=False
                return a
            if data == 'kill' :
                print("fermeture de la session")
                reply = 'kill'
                client_socket.send(reply.encode())
                client_socket.close()
                a= False
                return a
            if data == 'reset':
                print("fermeture de la session")
                reply = 'reset'
                client_socket.send(reply.encode())
                client_socket.close()
                a = False
                return a
            else:
                print("Serveur : ", data)
if __name__ == '__main__':
    a= True
    client_socket = socket.socket()
    client_socket.connect(('127.0.0.1', 8111))
    while a == True:
        try:
            data()
        except OSError:
            print(' Déconnexion')
            a = False
    client_socket.close()