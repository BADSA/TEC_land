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

from twisted.internet import reactor
from hostFactory import HostFactory
from host import Host
from connectionFinder import ConnectionFinder
from config import HostConfig
import argparse, threading


def chat(myuser):
    print "======================="
    print "|      HOST CHAT      |"
    print "======================="

    while True:
        to = raw_input("Receiver: ")
        text = raw_input("Write the message: ")
        data = {"type": 'm', "from": myuser, "to": to, "msg": text}
        host.send(data)

# Point of start for a TEC-Land Host
if __name__ == '__main__':
    parse = argparse.ArgumentParser()

    # Optional router ip & port to connect.
    parse.add_argument("-i", "--ip", type=str, help="Router's IP to connect.")
    parse.add_argument("-p", "--port", type=int, help="Router's port number to connect.")

    args = parse.parse_args()
    conMan = ConnectionFinder()
    host = Host(HostConfig.LISTENPORT)

    # Connect to given router
    myuser = ""
    if args.ip and args.port:
        myuser = host.connect(args.ip, args.port)
    else:
        print "Dynamic Binding"
        ip, port = conMan.look_for_router()
        if ip is not None:
            myuser = host.connect(ip, port)
        else:
            print "No routers available"

    # Test if thread is needed
    t = threading.Thread(target=chat, args=(myuser,))
    t.start()

    reactor.listenTCP(HostConfig.LISTENPORT, HostFactory())
    reactor.run()




