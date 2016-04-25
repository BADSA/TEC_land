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


class ChatClient(protocol.Protocol):
    """
    Protocol for the reception of messages
    in the host device.
    """

    def __init__(self):
        pass

    def dataReceived(self, data):
        """
        Responds to the event of data received in order
        to show the user the incoming message
        :param data: information received
        """

        data = json.loads(data)
        print "\n********************************"
        print "          New Message:         "
        print "'"+data["from"]+"'", "says", "'"+data["message"]+"'"
        print "********************************\n"
        self.transport.write("OK")
