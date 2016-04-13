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

import argparse
import csv, json, socket
from host import Host
from model.message import Message
from config import HostConfig


class ConnectionFinder:
    def __init__(self, wks=HostConfig.WKS):
        self.wks_file = wks
        self.routers = self.read_wks()

    def read_wks(self):  # Well Known Servers/Routers
        list = []
        with open(self.wks_file) as wks_file:
            fieldnames = ['name', 'ip', 'port']
            routers = csv.DictReader(wks_file, fieldnames=fieldnames)
            for router in routers:
                list.append(router)
        return list

    def look_for_router(self):
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
        data = json.loads(data)
        return [data["ip"], data["port"]]


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    # Optional router ip & port to connect.
    parse.add_argument("-i", "--ip", type=str, help="Router's IP to connect.")
    parse.add_argument("-p", "--port", type=int, help="Router's port number to connect.")
    args = parse.parse_args()
    conMan = ConnectionFinder()

    host = Host()
    # Connect to given router
    if args.ip and args.port:
        host.connect(args.ip, args.port)
    else:
        print "Dynamic Binding"
        ip, port = conMan.look_for_router()
        print "Voy pa {0}:{1}".format(ip, port)
        host.connect(ip, port)

    while 1:
        to = raw_input("Write the name of the username: ")
        text = raw_input("Write the message: ")
        mfrom = "melalonso"
        msg = Message(mfrom, to, text)
        host.send_message(msg)
