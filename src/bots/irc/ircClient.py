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
    nickname = "tecland"
    password = "tecland"

    def signedOn(self):
        # Called once the bot has connected to the IRC server
        self.join(self.factory.channel)

    def send(self, msg):
        print msg, "IRCCLIENT"
        data = json.loads(msg)

        self.msg("#{0}".format(self.factory.channel),
                 "{0} says {1}".format(data["from"], data["message"]))

