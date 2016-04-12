from time import sleep
from twisted.internet import protocol, reactor, defer
from client import RouterClient
import json
import csv


class RouterConnection(protocol.Protocol):
    # Routers file required
    def __init__(self, factory):
        self.factory = factory
        self.connection_type = ""
        self.username = ""
        self.router_count = 0
        self.routers = []

    def connectionMade(self):
        print "New Connection..."
        ##cself.factory.numConnections += 1

    def connectionLost(self, reason):
        print self.routers
        if self.connection_type == "r":
            self.factory.numConnections -= 1
            print "User {0} disconnected".format(self.username)
            self.factory.host_manager.delete(self.username)
        else:
            print "Connection lost"

    def dataReceived(self, data):
        # print data
        data = json.loads(data)
        self.connection_type = data["type"]
        self.parse_data(data)

    def parse_data(self, data):
        if data["type"] == 'r':
            self.register_ser(data)
        if data["type"] == 'q':
            self.get_connections()
        if data["type"] == 'n':
            self.ask_disp()
            print self.get_best_router()

    def register_user(self, data):
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

    def ask_disp(self):
        file_name = self.factory.routers_file
        with open(file_name, 'r') as routers_f:
            fieldnames = ['name', 'ip', 'port']
            routers = csv.DictReader(routers_f, fieldnames=fieldnames)
            for router in routers:
                rclient = RouterClient()
                reactor.connectTCP(router["ip"], int(router["port"]), rclient)
                response = rclient.get_response()
                d = response.addCallback(self.parse_response)
                print vars(d)

    def parse_response(self, response):
        return response

    def get_best_router(self):
        return self.routers

    def get_connections(self):
        self.transport.write(str(self.factory.numConnections))
