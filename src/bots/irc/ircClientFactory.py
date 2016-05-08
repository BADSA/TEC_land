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
    """ Create an IRC Client instance when a listener is created

    This class return an IRCClient instance to handle an TCP
    connection to a IRC server.

    This class also manage some configuration parameter like
    the channel to connect and brings an interface to communicate
    between the listener and the IRCClient to send messages.

    """
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        """ Create protocol IRCClient

        :param addr: Base usage parameter, not used in this class
        :return: An IRCClient instance.
        """
        self.proto = IRCClient()
        self.proto.factory = self
        return self.proto

    def clientConnectionLost(self, connector, reason):
        """ Reconnect connection got lost

        If there is a failure with the connection this
        methon will try to reconnect.

        :param connector: Previous active connection
        :param reason: Lost connection reason
        """
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        """ Stop current reactor

        Stop the reactor if the connection fails.

        :param connector: Previous active connection
        :param reason: Lost connection reason
        :return: """
        reactor.stop()

    def send(self, message):
        """ Send a message through the IRCClient

        This method wraps the IRCClient implementation of
        send method. It makes the IRCClient send method usable
        to the Listener class.

        :param message: String content of the data of the message to
        use send it to the IRCClient send method.
        :return:
        """
        self.proto.send(message)
