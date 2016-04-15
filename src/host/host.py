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

from twisted.internet import reactor, task
from hostFactory import HostFactory
from model.message import Message
import socket


class Host:

    def __init__(self):
        self.factory = HostFactory()

    def connect(self, ip, port):
        print "TEC-land host connecting to {0}:{1}".format(ip, port)
        s = socket.socket()
        s.connect((ip, port))
        print s.recv(1024)
        s.close()
