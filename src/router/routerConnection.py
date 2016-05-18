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
from twisted.internet.protocol import Protocol
from model.socketClient import SocketClient
from routerLinker import RouterLinker


class RouterConnection(Protocol):
    """
    This class handles every new connection to the router.

    On every connection the Factory will create an object of
    this class to handle the connection.

    This class is the responsible for send the messages over
    the local network, also connects to the other routers to
    now if some user exists on the net, forward messages to
    other routers or make broadcast over the entire NETWORK.

    """

    # Routers file required
    def __init__(self, factory):
        self.factory = factory
        self.connection_type = ""
        self.username = ""
        self.linker = None

    def connectionMade(self):
        """ Init and setup router connection

        It init the RouterLinker to manage the connection
        to the other routers, and build self router info.

        """
        print "New Connection..."
        self._build_router_info()
        self.linker = RouterLinker(self.factory.routers_file,
                                   {"ip": self.ip, "port": self.port},
                                   self.factory.numConnections,
                                   self.factory.host_manager)

    def connectionLost(self, reason):
        """ Notifies if connection got lost

        Handle if user got disconnected to erase it from
        the active users list.

        """
        if self.username:
            self.factory.numConnections -= 1
            print "User {0} disconnected".format(self.username)
            self.factory.host_manager.delete(self.username)
        else:
            print "Connection lost", "Connection type", self.connection_type, self.username

    def dataReceived(self, data):
        """ Receive data from any connection

        This method receive all messages and connection types,
        then it's send to the parser to take the corresponding
        action.

        :param data: string with information to connect or make
        an action over the router.

        """
        data = json.loads(data)
        self.connection_type = data["type"]
        self.parse_data(data)

    def parse_data(self, data):
        """ Chose which action take given a connection type.

        The description of each connection type will be given
        on the corresponding function called.

        :param data: This object should be a dictionary with
        all the message data, if there is not connection type
        provided any action will be taken.
        """
        if data["type"] == "b":
            self._check_hashtags(data)
        elif data["type"] == "bl":
            self._broadcast_local(data)
        elif data["type"] == "m":
            self.send_message(data)
        elif data["type"] == 'r':
            self.register_user(data)
        elif data["type"] == 'q':
            self.get_connections()
        elif data["type"] == 'n':
            router = self.linker.get_best_router()
            self._write(router)
        elif data["type"] == 'qu':  # query if user exists in local network
            self.is_local_user(data["username"])
        elif data["type"] == 'm':
            self.send_message(data)
        elif data["type"] == 'fw':
            self._send_to(data)
            self._write({"msg": "Message Delivered"})
        elif data["type"] == "rb":
            response, status = self.linker.look_place_for_bot(data)
            self._write(response, status)
        elif data["type"] == "rbl":
            self.register_bot(data)
        elif data["type"] == "sirc":
            data["to"] = "ircbot"
            self._send_to(data)
        else:
            self.transport.write("I don't know what to do with that.")

    def register_user(self, data):
        """ Register an user, username should be given.

        The method verifies if the username given it's already
        taken, if taken return a message with -1 status to
        try with another username, it also check if the same
        username already exists over the entire network to
        avoid duplicates. In the same way -1 will be sent if
        username already exits on the network.

        :param data: A dictionary with the username to register.
        """
        ip, _ = self.transport.client

        if not self.factory.host_manager.exists(data["username"]):
            router = self.linker.user_on_network(data["username"])
            # print router, "Existence in router", data
            if not router:
                self.username = data["username"]
                connection = {"ip": ip, "port": data["port"], "username": data["username"]}
                self.factory.host_manager.register(connection)
                self._write({"msg": "Username registered correctly"})
                print "User", self.username, "online."
                self.factory.numConnections += 1
                return

        self._write({"msg": "Username already taken"}, -1)
        self.username = ""

    def register_bot(self, data):
        """ Register bot on the router

        Take bot information to add it to the active hosts
        in the router.

        :param data: bot identification data

        """
        ip, _ = self.transport.client
        connection = {"ip": ip, "port": data["port"], "username": data["username"]}
        self.factory.host_manager.register(connection)
        self._write({"msg": "Registration successfully."})

    def get_connections(self):
        """ Get active connections on the router

        Return the number of active connection on the router.

        """
        self.transport.write(str(self.factory.numConnections))

    def is_local_user(self, username):
        """ Return if user exists on router

        Ask the HostManager if user is currently registered
        on the router.

        It response true of false to the questioner.

        :param username: the username which is going to be verified.
        """
        exists = self.factory.host_manager.exists(username)
        self._write({'exists': exists})

    def send_message(self, data):
        """ Check and send message if user exists

        It checks if the receiver exists on the network,
        and if send the message with _send_data method.
        If not notifies that the user to send the message
        is not reachable.

        :param data: object with the message, the sender and
        the receiver information to send the message.
        """
        if self.factory.host_manager.exists(data["to"]):
            # print data
            self._send_to(data)
            self._write({"msg": "Message Delivered"})
        else:
            print "Consulting routers to user"
            response = self.linker.user_on_network(data["to"])
            if response:
                data["type"] = 'fw'
                sc = SocketClient(self.response["ip"], self.response["port"], 1)
                response = sc.send(data)
                response = json.loads(response)
                self._write({"msg": response["msg"]}, response["status"])
            else:
                self._write({"msg": "Receiver is not reachable"}, -1)

    def _send_to(self, data, user_info=None):
        """ Send data to other host

        Send data with a SocketClient instance,
        it connects and send the desired message.

        If not user_info provided the method will
        fetch the information with the HostManager.

        :param data: message to send and sender identification.
        :param user_info: receiver identification data.

        """
        if not user_info:
            user_info = self.factory.host_manager.get_user(data["to"])

        sc = SocketClient(user_info["ip"], user_info["port"], 1)
        sc.send(data)

    def _build_router_info(self):
        """ Extract host ip and port

        Take host information from transport getHost method.
        The router now will know it's own ip(most important
        because port was given as a parameter) and port.

        """
        host = str(self.transport.getHost()).replace(')', '').split(', ')
        self.ip = host[1].replace("'", "")
        self.port = int(host[2])

    def _write(self, data, status=1):
        """ Send data to connected host

        This method send data to active connections,
        also provide an status to know if any action took
        before was successfully or not.

        :param data: data to send.
        :param status: optional if something wrong happens
        need to be set negative (-1).

        """
        # print data
        data["status"] = status
        self.transport.write(json.dumps(data))

    def _broadcast_local(self, data):
        """ Send message to local users

        The router will send a message to all users registered
        on the current router.

        :param data: object with the message to send and the sender.

        """
        local_users = self.factory.host_manager.get_users()
        for user in local_users:
            if "bot" not in user["username"]:
                self._send_to(data, user)

    def _check_hashtags(self, data):
        """ Check hashtag type

        Take an action depending of the hashtags provided.
        It will send the message to be broadcasted or to
        the selected bot.

        :param data: object with message and user identification.

        """
        hashtags = data["hashtags"]
        if "#itsATrap" in hashtags and "#publico" in hashtags:
            # TODO broadcast to nntp
            self._broadcast(data)
            msg, status = self.linker.send_to_irc(data)
            self._write(msg, status)

        elif "#publico" in hashtags:
            self._broadcast(data)
            msg, status = self.linker.send_to_irc(data)
            self._write(msg, status)

        elif "#itsATrap" in hashtags:
            self._broadcast(data)
            self._write({"msg": "Message Delivered"})
        else:
            self._write({"msg": "No valid hashtags provided"}, -1)

    def _broadcast(self, data):
        """ Send message to all the network

        This method broadcast any message all over the
        network, it also send the message to the other
        routers to deliver the message to all the user
        actively registered.

        :param data: sender and message to deliver over
        the network.

        """
        self._broadcast_local(data)
        self.linker.broadcast(data)
