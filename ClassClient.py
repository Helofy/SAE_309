import socket, threading, sys
msg =''
class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.thread = None

    def connect(self) -> int:
        try:
            self.sock.connect((self.host, self.port))
        except ConnectionRefusedError:
            print("serveur non lancé ou mauvaise information")
            return -1
        except ConnectionError:
            print("erreur de connection")
            return -1
        else:
            print("connexion réalisée")
            thread = threading.Thread(target=self.dialogue)
            thread.start()
            return 0
    def dialogue(self,msg):
        self.sock.send(msg.encode())
        awnser = self.sock.recv(1024).decode()
        print(awnser)
        return awnser

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) < 3:
    # idem code précédent
        print('hello')
    # en dehors du if
    Client.connect()
    message = ''

