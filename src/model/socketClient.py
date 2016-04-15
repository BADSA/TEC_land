from socket import socket, AF_INET, SOCK_STREAM, error
import json


class SocketClient:

    def __init__(self, ip, port, type=0):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.ip = ip
        self.type = type
        if isinstance(port, int):
            self.port = port
        else:
            try:
                self.port = int(port)
            except ValueError:
                raise ValueError

        self.con_info = (self.ip, self.port)

        self.is_connected = self._connect()  # se conecta cuando se inicializa el objeto

    def _connect(self):
        try:
            self.sock.connect(self.con_info)
            return True
        except error:
            return False

    def send(self, data):  # El send responde de una vez no necesita hacer recv
        self.sock.send(json.dumps(data))
        if self.type == 1:
            response = self.sock.recv(2048)
            self.sock.close()
            return response
        else:
            return self.sock.recv(2048)

    def close(self):
        self.sock.close()

    def status(self):  # Para verificar si la conexion se realiz`o
        return self.is_connected


