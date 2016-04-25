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
from model.socketClient import SocketClient


# Class that controls the task for a router
# Connects to a Router and send a message to a user
class Host:

    def __init__(self, ip, port):
        self.sock_client = SocketClient(ip, port)
        print "TEC-land network online..."
        print "TEC-land host connecting to {0}:{1}".format(ip, port)

    def send(self, msg):
        response = ""
        try:
            response = self.sock_client.send(msg)
        except:
            print 'Could not send to {}:{}\n'.format(self.router_ip, self.router_port)
            return None

        response = json.loads(response)

        return response

    def register_user(self, listen_port):
        username = raw_input("Please write an username to use: ")
        data = {"type": 'r', "username": username, "port": listen_port}
        response = self.send(data)
        if response["status"] == -1:
            print response["msg"]
            return self.register_user(listen_port)
        return username
