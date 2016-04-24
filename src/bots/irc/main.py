

import argparse

import json

from server.ircListeningFactory import IRCListenerFactory
from host.connectionFinder import ConnectionFinder
from model.socketClient import SocketClient
from twisted.internet import reactor
def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("-p", type=int, help="Listening port")
    args.add_argument("-n", type=str, help="Network to connect irc", default="localhost")
    args.add_argument("-c", type=str, help="Channel to connect irc", default="publico")
    args.add_argument("-irc_p", type=int, help="Port to connect irc server")
    return args.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print args
    irc = IRCListenerFactory(args.n, args.irc_p, args.c)
    ip, port = ConnectionFinder("routers.csv").look_for_router()
    sc = SocketClient(ip, port, 1)
    response = sc.send({"type": "rb", "bot_type": "ircbot"})
    response = json.loads(response)
    # TODO validations if there can not be more irc bots on the network
    sc = SocketClient(response["ip"], response["port"], 1)
    print "TODO BIEN HASTA AQUI"
    response = sc.send({"type": 'rbl', "username": "ircbot", "port": args.p})

    response = json.loads(response)

    print response["msg"]

    reactor.listenTCP(args.p, irc)
    reactor.run()