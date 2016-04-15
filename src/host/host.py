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

import socket
import json


# Class that controls the task for a router
# Connects to a Router and send a message to a user
class Host:

    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenPort = port
        print "TEC-land network online..."

    def connect(self, ip, port):
        print "TEC-land host connecting to {0}:{1}".format(ip, port)
        self.sock.connect((ip, int(port)))
        return self._register_user()

    def send(self, msg):
        msg = json.dumps(msg)
        try:
            self.sock.send(msg)
        except:
            print 'Could not send to {}:{}\n'.format(self.router_ip, self.router_port)
            return None
        response = self.sock.recv(2048)
        response = json.loads(response)
        print response["msg"]
        return response

    def _register_user(self):
        username = raw_input("Please write an username to use: ")
        data = {"type": 'r', "username": username, "port": self.listenPort}
        response = self.send(data)
        if response["msg"] == "NO":
            print "Username already taken, choose another one."
            self._register_user()
        return username
