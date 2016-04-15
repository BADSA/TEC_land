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

from twisted.internet import reactor, protocol, task
import json


class ChatClient(protocol.Protocol):

    def connectionMade(self):
        print "Connection made"
        self.register_user()

    def dataReceived(self, data):
        print "***********************"
        print "New message received: "
        print data
        print "***********************"

    def register_user(self):
        print "TEC-land network online..."
        username = raw_input("Please write an username to use: ")
        data = {"type": 'r', "username": username}
        self.transport.write(json.dumps(data))

    def send_data(self, data):
        print "Voy a mandar"
        print data
        print "==============="
        self.transport.write(json.dumps(data))
