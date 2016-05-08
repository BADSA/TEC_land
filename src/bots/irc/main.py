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

import argparse
import json
from twisted.internet import reactor
from ircListeningFactory import IRCListenerFactory
from host.connectionFinder import ConnectionFinder
from model.socketClient import SocketClient

"""
    This file manage the execution of the IRC bot
"""

def parse_args():
    """ Parse arguments given to the program

    This method parse and verifies that the given arguments
    are correct. And that all the necessary parameters where
    supplied when the program was called.

    :return: An object containing parsed given parameters
    """
    args = argparse.ArgumentParser()
    args.add_argument("-p", type=int, help="Listening port")
    args.add_argument("-n", type=str, help="Network to connect irc", default="localhost")
    args.add_argument("-c", type=str, help="Channel to connect irc", default="publico")
    args.add_argument("-irc_p", type=int, help="Port to connect irc server")
    return args.parse_args()

if __name__ == '__main__':
    """ Main execution flow

    This is the main execution to make the IRC bot work

    It find an suitable router and receive a router ID data,
    then it connects to the router to register the bot.

    Then it initialize the necessary classes with the given
    parameters and create a new reactor to handle every
    event with it corresponding protocol event handler.

    It keeps listening data from the port and send it to
    the IRC server.

    It keep the reactor thread running on the main thread.
    (Twisted stuff).
    """
    args = parse_args()
    irc = IRCListenerFactory(args.n, args.irc_p, args.c)
    ip, port = ConnectionFinder("routers.csv").look_for_router()
    sc = SocketClient(ip, port, 1)
    response = sc.send({"type": "rb", "bot_type": "ircbot"})
    response = json.loads(response)
    if response["status"] == -1:
        print response["msg"]
    else:
        sc = SocketClient(response["ip"], response["port"], 1)
        response = sc.send({"type": 'rbl', "username": "ircbot", "port": args.p})

        response = json.loads(response)

        print response["msg"]

        reactor.listenTCP(args.p, irc)
        reactor.run()
