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

class Listener(protocol.Protocol):

    def dataReceived(self, data):
        self.factory.client.send(data)
        self.transport.write(json.dumps({'msg': 'Message delivered successfully'}))
