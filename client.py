import socket
import threading
from game import Screen

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))

def receiver():
    while 1:
        a = input()
        clientsocket.send(a.encode())

def sender():
    while 1:
        a = clientsocket.recv(100000)
