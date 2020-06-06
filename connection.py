import json
import socket


class Connection:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 8080))
        self.running = True
        self.buff_size = 2 ** 15

    def receive(self, state):
        while self.running:
            state.data = json.JSONDecoder().decode(self.socket.recv(self.buff_size).decode())
            if state.data is not None:
                state.do_update = True

    def send(self, data):
        self.socket.send(data.encode())