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
from ircClient import IRCClient


class IRCClientFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        self.proto = IRCClient()
        self.proto.factory = self
        return self.proto

    def clientConnectionLost(self, connector, reason):
        # Try to reconnect if disconnected.
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def send(self, message):
        self.proto.send(message)
