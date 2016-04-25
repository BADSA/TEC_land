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
from chatClient import ChatClient


class HostFactory(protocol.Factory):
    """
    Factory that allows to handle the
    host incoming messages.
    """

    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return ChatClient()
