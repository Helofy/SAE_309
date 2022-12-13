import socket, threading, sys


class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.thread = None

    # fonction de connection.
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
            thread = threading.Thread(target=self.reception)
            thread.start()
            return 0

    """ 
        fonction qui gére le dialogue
        -> lance une thread pour la partie reception 
        -> lance une boucle pour la partie emission. arréte si kill, reset ou disconnect
    """



    def envoi(self,msg):
        self.sock.send(msg.encode())

    """
      thread recepction, la connection étant passée en argument
    """

    def reception(self,):
        msg = ""
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = self.sock.recv(1024).decode()
            print(msg)


if __name__ == "__main__":

    print(sys.argv)
    if len(sys.argv) < 3:
    # idem code précédent
        print('hello')
    # en dehors du if
    Client.connect()
    message = ''

