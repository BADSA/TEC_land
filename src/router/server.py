import argparse
import json
from twisted.internet import protocol, reactor
from model.hostManager import HostManager


class Router(protocol.Protocol):

    # Routers file required
    def __init__(self, factory):
        self.factory = factory
        self.username = ""

    def connectionMade(self):
        self.factory.numConnections += 1

    def connectionLost(self, reason):
        print "User {0} disconnected".format(self.username)
        self.factory.host_manager.delete(self.username)
        self.factory.numConnections -= 1

    def dataReceived(self, data):
        data = json.loads(data)
        if data["type"] == 'r':
            self.username = data["username"]
            self.transport.write("Registering User...")
            ip, port = self.transport.client
            connection = {"ip": ip, "port": port, "username": data["username"]}
            if not self.factory.host_manager.exists(data["username"]):
                self.factory.host_manager.register(connection)
                self.transport.write("Username registered correctly")
            else:
                self.transport.write("Username already taken")
                self.username = ""
        else:
            self.transport.write("Not supported")

    def parse_data(self, data):
        pass


class RouterFactory(protocol.Factory):

    def __init__(self, r_file):
        self.host_manager = HostManager()
        self.routers_file = r_file
        self.numConnections = 0

    def buildProtocol(self, addr):
        return Router(self)


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-p", type=int,  help="router port number")
    parse.add_argument("-f", type=argparse.FileType('r'),  help="routers ip and ports file", default="routers")
    args = parse.parse_args()
    reactor.listenTCP(args.p, RouterFactory(args.f))
    print "TEC-land router up on port: {0}".format(args.p)
    reactor.run()

