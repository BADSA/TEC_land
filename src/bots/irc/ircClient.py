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

from twisted.words.protocols import irc
import json


class IRCClient(irc.IRCClient):
    """ Class to send messages to an IRC channel

    This class will be instanced when an listener instance
    is created, it will connect to a IRC server and will
    join a channel to publish all broadcasted messages.

    """
    nickname = "tecland"
    password = "tecland"

    def signedOn(self):
        """ Join the bot to a channel once it got segnedOn

        Once the bot succefully connects to the IRC server
        it joins a channel previously set on the factory class

        """
        # Called once the bot has connected to the IRC server
        self.join(self.factory.channel)

    def send(self, msg):
        """ Send message to the channel

        This method receive a message data, it parse the msg
        parameter to obtain the message and the sender.

        The message will be formatted to contain the sender
        and the message that the user wanted to transmit.

        :param msg: JSON string containing the sender and
        the message to transmit.

        """
        print msg, "IRCCLIENT"
        data = json.loads(msg)

        self.msg("#{0}".format(self.factory.channel),
                 "{0} says {1}".format(data["from"], data["message"]))

