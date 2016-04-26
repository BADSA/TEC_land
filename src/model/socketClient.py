# coding=utf-8
"""
Instituto Tecnológico de Costa Rica
Ingeniería en Computación
Redes de Computadoras
Profesor: Kevin Moraga
Estudiantes:
    Daniel Solís Méndez
    Melvin Elizondo Pérez
I Semestre 2016
"""

from socket import socket, AF_INET, SOCK_STREAM, error
import json


class SocketClient:
    """
    Class that takes responsibility on the sockets
    to connect to a router and send any message.
    """

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

        # Connect to initialize socket
        self.is_connected = self._connect()

    def _connect(self):
        """
        Connects to ip and port given in initialize.
        :return: True or False
        """

        try:
            self.sock.connect(self.con_info)
            print "TEC-land network online..."
            print "TEC-land host connecting to {0}:{1}".format(self.ip, self.port)
            return True
        except error:
            return False

    def send(self, data):
        """
        Sends a message to the routers and waits for its response
        :param data: Data to send in the message
        :return: the response obtained from the router
        """
        data = json.dumps(data)
        self.sock.send(data)
        if self.type == 1:
            response = self.sock.recv(2048)
            self.sock.close()
            return response
        else:
            return self.sock.recv(2048)

    def close(self):
        """
        Closes the connection.
        """
        self.sock.close()

    def status(self):
        """
        Check status of the connection.
        :return: True if the connection was successful, False if not.
        """
        return self.is_connected
