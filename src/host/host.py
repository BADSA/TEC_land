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


class Host:

    def __init__(self):
        self.router_ip = ""
        self.router_port = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "TEC-land network online..."
        self.register_user()

    def connect(self, ip, port):
        print "TEC-land host connecting to {0}:{1}".format(ip, port)
        self.sock.connect((ip, port))
        self.router_ip = ip
        self.router_port = port

    def send(self, msg):
        try:
            self.sock.send(msg)
        except:
            print 'Could not send to {}:{}\n'.format(self.router_ip, self.router_port)
            return None
        response = self.sock.recv(2048)
        return response

    def register_user(self):
        username = raw_input("Please write an username to use: ")
        data = {"type": 'r', "username": username}
        response = self.send(json.dumps(data))
        if response == "NO":
            print "Username already taken, choose another one."
            self.register_user()
