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
from chatClient import ChatClient


class HostFactory(protocol.ClientFactory):

    def __init__(self):
        self.p = ChatClient()
        self.p.factory = self

    def buildProtocol(self, addr):
        return self.p

    def ask_for_msg(self):
        to = raw_input("Receiver: ")
        text = raw_input("Write the message: ")
        mfrom = "melalonso"
        data = {"from": mfrom, "to": to, "msg": text}
        self.p.send_data(data)

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed."
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost."
        reactor.stop()
