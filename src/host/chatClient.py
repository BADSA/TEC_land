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

from twisted.internet import protocol
import json

# Protocol for the reception of messages
class ChatClient(protocol.Protocol):

    def __init__(self):
        pass

    def dataReceived(self, data):
        data = json.loads(data)
        print "\n********************************"
        print "          New Message:         "
        print "'"+data["from"]+"'", "says", "'"+data["message"]+"'"
        print "********************************\n"
        self.transport.write("Got your message")
