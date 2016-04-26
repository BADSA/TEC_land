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

import json
from model.message import Message
from model.socketClient import SocketClient


class MessageSender:
    """
    Class that handles sending messages to
    other nodes in the networks, using the
    receiver's username.
    """

    def __init__(self, ip, port):
        self.sc = SocketClient(ip, port)

    def ask_message(self, user):
        """
        Function that runs in a Thread to keep
        asking the host for the message to send.
        :param user: host username to include as sender
        :return: response message
        """

        print "======================="
        print "|      HOST CHAT      |"
        print "======================="

        while True:
            text = raw_input("Write the message: ")
            if "#" not in text:
                to = raw_input("Receiver: ")
                data = Message(user, to, text).to_dict()
                response = self.send(data)
            else:
                data = Message(user, None, text, 'b').to_dict()
                response = self.send(data)

            if response["status"] == -1:
                print ""
                print response["msg"]
                print ""

    def send(self, msg):
        """
        Sends message to the router with help of the socket client.
        :param msg: data to send.
        :return: response if sent, None if error.
        """
        try:
            response = self.sc.send(msg)
        except:
            print 'Could not send message\n'
            return None

        response = json.loads(response)

        return response
