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
    """ Class to handle received data

     This class receive data from the router and redirect it
     to the IRC server through an IRCClient

    """

    def dataReceived(self, data):
        """ Receive data en send it to the IRC Server

        This method parse the received data to send it to the IRC
        server.

        It basically only redirect the received data through the
        client.

        :param data: String with the received data
        """
        self.factory.client.send(data)
        self.transport.write(json.dumps({'msg': 'Message delivered successfully'}))
