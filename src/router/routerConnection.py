from twisted.internet import protocol, reactor, defer
from model.socketClient import SocketClient
import json
import csv


class RouterConnection(protocol.Protocol):
    # Routers file required
    def __init__(self, factory):
        self.factory = factory
        self.connection_type = ""
        self.username = ""
        self.routers = []
        self.response = None

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
        data = json.loads(data)
        self.connection_type = data["type"]
        self.parse_data(data)

    def parse_data(self, data):
        if data["type"] == "m":
            self.send_message(data)
        elif data["type"] == 'r':
            self.register_user(data)
        elif data["type"] == 'q':
            self.get_connections()
        elif data["type"] == 'n':
            self.routers = []
            self._consult_routers({"type": "q"}, self.ask_disp)
            self._get_best_router()
        elif data["type"] == 'qu': #query if user exists in local network
            self.is_local_user(data["username"])
        elif data["type"] == 'm':
            self.send_message(data)
        elif data["type"] == 'fw':
            self._send_to(data)
        else:
            self.transport.write("I don't know what to do with that.")

    def register_user(self, data):
        ip, _ = self.transport.client

        if not self.factory.host_manager.exists(data["username"]):
            self._consult_routers({"type": 'qu', "username": data["username"]}, self.user_on_router)
            if not self.response:
                self.username = data["username"]
                connection = {"ip": ip, "port": data["port"], "username": data["username"]}
                self.factory.host_manager.register(connection)
                self._write({"msg": "Username registered correctly"})
                self.factory.numConnections += 1
                return

        self._write({"msg": "Username already taken"}, -1)
        self.username = ""

    def _consult_routers(self, data, func):
        self.response = None
        file_name = self.factory.routers_file
        with open(file_name, 'r') as routers_f:
            fieldnames = ['name', 'ip', 'port']
            routers = csv.DictReader(routers_f, fieldnames=fieldnames)
            for router in routers:
                sc = SocketClient(router["ip"], router["port"], 1)
                if sc.status():
                    response = sc.send(data)
                    if func(router, response):
                        break

    def ask_disp(self, router, response):
        self.routers.append([router, int(response)])

    def parse_response(self, response):
        self.factory.routers.append(response)

    def user_on_router(self, router, response):
        response = json.loads(response)
        if response["exists"]:
            self.response = router
            return True

    def get_connections(self):
        self.transport.write(str(self.factory.numConnections))

    def is_local_user(self, username):
        exists = self.factory.host_manager.exists(username)
        self._write({'exists': exists})

    def send_message(self, data):
        if self.factory.host_manager.exists(data["to"]):
            self._send_to(data)
            #self._write({"msg": "Send successfully"})
        else:
            print "Consulting routers to user"
            self._consult_routers({"type": 'qu', "username": data["to"]}, self.user_on_router)
            if self.response:
                data["type"] = 'fw'
                sc = SocketClient(self.response["ip"], self.response["port"], 1)
                response = sc.send(data)
                response = json.loads(response)
                self._write({"msg": response["msg"]}, response["status"])
            else:
                self._write({"msg": "Receiver is not reachable"}, -1)

    def _send_to(self, data):
        user_info = self.factory.host_manager.get_user(data["to"])
        sc = SocketClient(user_info["ip"], user_info["port"], 1)
        response = sc.send(data)
        print response, "FUNTION _SENT_TO"
        self._write({"msg": "Message Delivered"})

    def _get_best_router(self):

        if not self.routers:
            self._write({"ip": self.ip, "port": self.port})
            return

        better = self.routers[0]

        for router in self.routers:
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

    def _write(self, data, status=1):
        data["status"] = status
        self.transport.write(json.dumps(data))
