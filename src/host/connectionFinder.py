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

import csv, json, socket
from config import HostConfig


# Class that looks for an available
# router and asks for the router
# with less connections.
class ConnectionFinder:
    def __init__(self, wks=HostConfig.WKS):
        self.wks_file = wks
        self.routers = self.read_wks()

    # Reads the Well Known Servers/Routers
    def read_wks(self):
        list = []
        with open(self.wks_file) as wks_file:
            fieldnames = ['name', 'ip', 'port']
            routers = csv.DictReader(wks_file, fieldnames=fieldnames)
            for router in routers:
                list.append(router)
        return list

    # Ask what router should the host connect
    def look_for_router(self):
        found = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for router in self.routers:
            try:
                ip = router["ip"]
                port = int(router["port"])
                s.connect((ip, port))
                print "Server %s is up and running!" % router["ip"]
                s.sendto(json.dumps({"type": 'n'}), (ip, port))
                found = True
                break
            except socket.error as e:
                print "Server %s is not running" % router["ip"]
        if found:
            data = s.recv(2048)
            data = json.loads(data)
            s.close()
            return [data["ip"], data["port"]]

        s.close()
        return [None, None]
