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

from helperRouter import Router
import argparse
import csv, json, socket


class ConnectionManager:
    def __init__(self, wks="routers.csv"):
        self.wks_file = wks
        self.routers = self.readWKS()
        self.helperRouter = Router()

    def readWKS(self):  # Well Known Servers/Routers
        list = []
        with open(self.wks_file) as wks_file:
            fieldnames = ['name', 'ip', 'port']
            routers = csv.DictReader(wks_file, fieldnames=fieldnames)
            for router in routers:
                list.append(router)
        return list

    def lookForRouter(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for router in self.routers:
            try:
                ip = router["ip"]
                port = int(router["port"])
                s.connect((ip, port))
                print "Server %s is up and running!" % router["ip"]
                s.sendto(json.dumps({"type": 'n'}), (ip, port))
                break
            except socket.error as e:
                print "Server %s is not running" % router["ip"]

        data = s.recv(2048)
        s.close()
        return [data["ip"], data["port"]]

    @staticmethod
    def connect(ip, port):
        print "TEC-land host connecting to {0}:{1}".format(ip, port)
        # reactor.connectTCP(ip, port, HostFactory())
        # reactor.run()


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    # Optional router ip & port to connect.
    parse.add_argument("-i", "--ip", type=str, help="Router's IP to connect.")
    parse.add_argument("-p", "--port", type=int, help="Router's port number to connect.")
    parse.add_argument("-f", "--file", type=argparse.FileType('r'), help="Routers' ip and port file",
                       default="routers.csv")
    args = parse.parse_args()
    conMan = ConnectionManager()

    # Connect to given router
    if args.ip and args.port:
        conMan.connect(args.ip, args.port)
    else:
        print "Dynamic Binding"
        ip, port = conMan.lookForRouter()
        conMan.connect(ip, port)
