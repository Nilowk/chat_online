import socket as s
import os
import threading


class Server:

    def __init__(self, ip):
        self.clients = {}
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket.bind((ip, 64599))
        self.socket.listen(4)
        threading.Thread(name="accept", target=lambda: self.accept_connections()).start()
        threading.Thread(name="cmd", target=lambda: self.server_cmd()).start()

        i = 0
        while True:
            if len(self.clients) > 0:
                if i >= len(self.clients):
                    i = 0
                if not self.clients[list(self.clients.keys())[i]]:
                    self.clients[list(self.clients.keys())[i]] = True
                    threading.Thread(name="receive", target=lambda: self.receive_data(list(self.clients.keys())[i])).start()
                i += 1

    def server_cmd(self):
        while True:
            cmd = str(input("cmd > "))
            if cmd == "stop":
                os._exit(1)

    def receive_data(self, client):
        index = 0
        while True:
            try:
                index = self.clients[client].__index__()
                data = client.recv(1024)
                if data:
                    for i in range(len(self.clients)):
                        if not (client == list(self.clients.keys())[i]):
                            list(self.clients.keys())[i].send(data)
            except (ConnectionResetError, KeyError):
                self.clients.pop(list(self.clients.keys())[index])
                print(index)

    def accept_connections(self):
        while True:
            connexion, address = self.socket.accept()
            self.clients[connexion] = False

