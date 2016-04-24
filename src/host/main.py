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

from model.message import Message


def chat(myuser):
    print "======================="
    print "|      HOST CHAT      |"
    print "======================="

    while True:
        text = raw_input("Write the message: ")
        if "#" not in text:
            to = raw_input("Receiver: ")
            data = Message(myuser, to, text).to_dict()
            host.send(data)
        else:
            data = Message(myuser, None, text, 'b').to_dict()
            host.send(data)

# Point of start for a TEC-Land Host
if __name__ == '__main__':
    parse = argparse.ArgumentParser()

    # Optional router ip & port to connect.
    parse.add_argument("-i", "--ip", type=str, help="Router's IP to connect.")
    parse.add_argument("-p", "--port", type=int, help="Router's port number to connect.")

    args = parse.parse_args()
    conMan = ConnectionFinder()

    # Connect to given router
    myuser = ""
    if args.ip and args.port:
        host = Host(args.ip, args.port)
        myuser = host.register_user()
    else:
        print "Dynamic Binding"
        ip, port = conMan.look_for_router()
        host = Host(ip, port)
        if ip is not None:
            myuser = host.register_user(HostConfig.LISTENPORT)
        else:
            print "No routers available"

    # Test if thread is needed
    t = threading.Thread(target=chat, args=(myuser,))
    t.start()

    reactor.listenTCP(HostConfig.LISTENPORT, HostFactory())
    reactor.run()




