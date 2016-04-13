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

from twisted.internet import reactor, protocol
import json


class ChatClient(protocol.Protocol):
    def connectionMade(self):
        self.registerUser()

    def dataReceived(self, data):
        print data
        # self.transport.loseConnection()

    def registerUser(self):
        print "TEC-land network online..."
        username = raw_input("Please write an username to use: ")
        data = {"type": 'r', "username": username}
        self.transport.write(json.dumps(data))

    def getRouterIp(self):
        pass