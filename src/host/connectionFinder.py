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
from config import HostConfig
from model.socketClient import SocketClient


class ConnectionFinder:
    """
    Class that looks for an available
    router and asks for the router
    with less connections.
    """

    def __init__(self, wks=HostConfig.WKS):
        self.wks_file = wks
        self.routers = self.read_wks()

    def read_wks(self):
        """
        Reads the Well Known Servers/Routers
        :return: list with WKS
        """
        list = []
        with open(self.wks_file) as wks_file:
            fieldnames = ['name', 'ip', 'port']
            routers = csv.DictReader(wks_file, fieldnames=fieldnames)
            for router in routers:
                list.append(router)
        return list

    def look_for_router(self):
        """
        Looks for the router the host should connect
        :return: [ip, port] if found, [none, none] if not
        """
        found = False
        s = None
        for router in self.routers:
                ip = router["ip"]
                port = int(router["port"])
                s = SocketClient(ip, port)
                if s.status():
                    print "TEC-land network online..."
                    print "TEC-land host connecting to {0}:{1}".format(ip, port)
                    print "Server {0} is up and running on port {1}".format(router["ip"], router["port"])
                    found = True
                    break
                print "Server %s is not running" % router["ip"]
        if found:
            data = s.send({"type": 'n'})
            data = json.loads(data)
            s.close()
            return [data["ip"], data["port"]]
        if s:
            s.close()
        return [None, None]
