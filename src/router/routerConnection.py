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

    def connectionMade(self):
        print "New Connection..."
        self._build_router_info()

    def connectionLost(self, reason):
        if self.connection_type == "r":
            self.factory.numConnections -= 1
            print "User {0} disconnected".format(self.username)
            self.factory.host_manager.delete(self.username)
        else:
            print "Connection lost"

    def dataReceived(self, data):
        print "Recibi ", data
        print type(data)
        data = json.loads(data)
        print data
        self.connection_type = data["type"]
        self.parse_data(data)

    def parse_data(self, data):
        if data["type"] == "m":
            self.send_to_user(data)
        elif data["type"] == 'r':
            self.register_user(data)
        elif data["type"] == 'q':
            self.get_connections()
        elif data["type"] == 'n':
            # ip, port = getRouterLessCharged()
            # data = {"ip": ip, "port": port}
            data = {"ip": "127.0.0.1", "port": 8000}
            self.transport.write(json.dumps(data))
            # self.ask_disp()
            # print self.get_best_router()
        else:
            self.transport.write("I don't know what to do with that.")

    def register_user(self, data):
        self.username = data["username"]
        ip, port = self.transport.client
        connection = {"ip": ip, "port": port, "username": data["username"]}
        if not self.factory.host_manager.exists(data["username"]):
            self.factory.host_manager.register(connection)
            self._write({"msg": "Username registered correctly"})
            self.factory.numConnections += 1
        else:
            self._write({"msg": "Username already taken"})
            self.username = ""

    def send_to_user(self, data):
        self._write({"msg": "Message successfully sent"})

    def ask_disp(self):
        file_name = self.factory.routers_file
        routers_list = []
        with open(file_name, 'r') as routers_f:
            fieldnames = ['name', 'ip', 'port']
            routers = csv.DictReader(routers_f, fieldnames=fieldnames)
            for router in routers:
                rc = RouterClient(router["ip"], router["port"], 1)
                response = rc.send({"type": "q"})
                print router, "Cantidad de conexiones:", response
                routers_list.append([router, int(response)])

        if not routers_list:
            self._write({"ip": self.ip, "port": self.port})
        else:
            self._get_best_router(routers_list)

    def parse_response(self, response):
        self.factory.routers.append(response)

    def get_connections(self):
        self.transport.write(str(self.factory.numConnections))

    def _get_best_router(self, list):
        better = list[0]

        for router in list:
            if router[1] < better[1]:
                better = router

        if self.factory.numConnections < better[1]:
            self._write({"ip": self.ip, "port": self.port})
        else:
            self._write(better[0])

    def _build_router_info(self):
        host = str(self.transport.getHost()).replace(')', '').split(', ')

        self.ip = host[1].replace("'", "")
        self.port = int(host[2])

    def _write(self, data):
        self.transport.write(json.dumps(data))
