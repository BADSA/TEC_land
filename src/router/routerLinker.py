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

import csv
import json

from model.socketClient import SocketClient


class RouterLinker:

    def __init__(self, routers_f, router_info, num_connections, host_manager):
        self.host_manager = host_manager
        self.num_connections = num_connections
        self.routers_file = routers_f
        self.router_info = router_info
        self.routers = []
        self.response = None

    def get_best_router(self):
        self.routers = []
        self._send_to_routers({"type": "q"}, self.ask_disp)
        self._get_best_router()
        return self.response

    def user_on_network(self, username):
        self._send_to_routers({"type": 'qu', "username": username}, self._user_on_router)
        return self.response

    def send_to_routers(self, data):
        self._send_to_routers(data)

    def broadcast(self, data):
        self._broadcast_network(data)

    def send_to_irc(self, data):
        return self._send_to_irc(data)

    def _send_to_routers(self, data, func=None):
        """ Send data to all the routers on the network.

        This is a generic method to communicate with the other
        router in the network, it send a data object with a
        specific connection type and applies a function(if given)
        to the response given by the connected router.

        :param data: Should be a dictionary object which contains
        the connection type to decide an action and extra data if
        it's needed to complete the action.

        :param func: Should be a function with two parameters, the
        responding router and the response. Each function should
        determinate what to do with the response.

        """
        self.response = None
        file_name = self.routers_file
        with open(file_name, 'r') as routers_f:
            fieldnames = ['name', 'ip', 'port']
            routers = csv.DictReader(routers_f, fieldnames=fieldnames)
            for router in routers:
                sc = SocketClient(router["ip"], router["port"], 1)
                if sc.status():
                    response = sc.send(data)
                    if func and func(router, response):
                        break

    def ask_disp(self, router, response):
        self.routers.append([router, int(response)])

    def _user_on_router(self, router, response):
        response = json.loads(response)
        if response["exists"]:
            self.response = router
            return True

    def _get_best_router(self):
        if not self.routers:
            self.response = self.router_info
            return

        better = self.routers[0]

        for router in self.routers:
            if router[1] < better[1]:
                better = router

        if self.num_connections < better[1]:
            self.response = self.router_info
        else:
            self.response = better[0]

    def accept_bot(self, router, response):
        response = json.loads(response)
        if not response["exists"]:
            self.response = router
            return True

    def _broadcast_network(self, data):
        data["type"] = "bl"
        self._send_to_routers(data)

    def look_place_for_bot(self, data):
        if not self.host_manager.exists(data["bot_type"]):
            return self.router_info, 1
        else:
            self._send_to_routers({"type": "qu", "username": data["bot_type"]}, self.accept_bot)
            if self.response:
                return {"ip": self.response["ip"], "port": self.response["port"]}, 1
            else:
                return {"msg": "There is no more space left for IRC bots on the network"}, -1

    def _send_to_irc(self, data):
        if self.host_manager.exists("ircbot"):
            user_info = self.host_manager.get_user("ircbot")

            sc = SocketClient(user_info["ip"], user_info["port"], 1)
            if sc.status():
                response = sc.send({"message": data["message"], "from": data["from"]})
                response = json.loads(response)
                print "[IRCBOT]", response["msg"]
                return {"msg": "Message Delivered"}, 1

            else:
                self.host_manager.delete("ircbot")
                return self._send_to_irc(data)
        else:
            response = self.user_on_network("ircbot")
            if response:
                sc = SocketClient(self.response["ip"], self.response["port"], 1)
                data["type"] = 'sirc'
                response = json.loads(sc.send(data))
                # print response
                return {"msg": "Message Delivered"}, 1
            else:
                return {"msg": "IRC Service not available"}, -1
