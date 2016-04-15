import argparse, sys

from twisted.internet import protocol, reactor
from model.hostManager import HostManager
from routerConnection import RouterConnection


class Router(protocol.Factory):

    def __init__(self, r_file):
        self.host_manager = HostManager()
        self.routers_file = r_file
        self.numConnections = 0
        self.routers = []

    def buildProtocol(self, addr):
        return RouterConnection(self)


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-p", type=int,  help="router port number")
    parse.add_argument("-f", type=str,  help="routers ip and ports file", default="routers.csv")

    args = parse.parse_args()
    reactor.listenTCP(args.p, Router(args.f))
    print "TEC-land router up on port: {0}".format(args.p)
    reactor.run()

