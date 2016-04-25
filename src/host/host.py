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

import threading
from twisted.internet import reactor
from listener.hostFactory import HostFactory
from sender.messageSender import MessageSender
from config import HostConfig


class Host:
    """
    Class that starts the functions for a host.
    """

    def __init__(self, ip, port):
        self.msg_sender = MessageSender(ip, port)

    def start(self):
        """
        Initializes the host by registering the user,
        starting the msg_sender service and the listener
        for incoming messages.
        """
        my_user = self._register_user(HostConfig.LISTENPORT)

        t = threading.Thread(target=self.msg_sender.ask_message, args=(my_user,))
        t.start()

        reactor.listenTCP(HostConfig.LISTENPORT, HostFactory())
        reactor.run()

    def _register_user(self, listen_port):
        """
        Registers the username to use by the host.
        :param listen_port: where the incoming messages are going
        to be sent by the router.
        :return: accepted username.
        """
        username = raw_input("Please write an username to use: ")
        data = {"type": 'r', "username": username, "port": listen_port}
        response = self.msg_sender.send(data)
        if response["status"] == -1:
            print response["msg"]
            return self._register_user(listen_port)
        return username
