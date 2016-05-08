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

from twisted.internet import protocol, reactor
from ircClientFactory import IRCClientFactory
from listener import Listener


class IRCListenerFactory(protocol.Factory):
    """ Creates an Listener instance

    This class create an Listener instance to handle a
    TCP listener event to listen message from an specific
    router on the network.

    It also create an instance of to handle a TCP connection
    to connect to the IRC server to send broadcasted messages.
    """
    def __init__(self, network, irc_port, channel):
        """ Create the class instance and initialize TCP connection

        It create an TCP connection handler to connect to the IRC
        server by creating an IRCClientFactory instance.

        :param network: String containing the URI to the IRC network
        :param irc_port: Port to connect the IRC server
        :param channel: Channel to join when the connection to the
        server got successfully stabilised.
        """
        self.client = IRCClientFactory(channel)
        reactor.connectTCP(network, irc_port, self.client)

    def buildProtocol(self, addr):
        """ Create an Listener instance

        This method create an Listener instance to receive all the
        messages send from the router.

        :param addr: Method based implementation parameter. Not used here.
        :return: A Listener protocol instance.
        """
        self.proto = Listener()
        self.proto.factory = self
        return self.proto