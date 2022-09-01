import threading
import socket

class Terminal:
    def __init__(self, connection):
        self.connection = connection
        self.commands_incoming = []
        self.commands_outgoing = []
        listener = threading.Thread(target=self.listen)#, daemon=True)
        listener.start()
        sender = threading.Thread(target=self.send)
        sender.start()
        
    def getch(self, *args):
        if self.commands_incoming:
            return self.commands_incoming.pop(0)
        else:
            return -1

    def send(self):
        while 1:
            if self.commands_outgoing:
                self.connection.send(self.commands_outgoing.pop(0).encode())
        pass
    
    def listen(self):
        while 1:
            try:
                buf = self.connection.recv(128)
                if buf:
                    # raise Exception("HELLE")
                    self.commands_incoming.append(buf.decode())
            except BlockingIOError:
                pass
    
    def addstr(self, *args):
        pass

class Server(Terminal):
    def __init__(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(('localhost', 8089))
        serversocket.listen()
        connection, address = serversocket.accept()
        super().__init__(connection)

class Client(Terminal):
    def __init__(self):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 8089))
        super().__init__(clientsocket)
        