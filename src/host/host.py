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


class Host:

    def __init__(self):
        self.factory = HostFactory()

    def connect(self, ip, port):
        print "TEC-land host connecting to {0}:{1}".format(ip, port)
        reactor.connectTCP(ip, port, self.factory)
        reactor.run()

    def send_message(self, msg):
        data = {"from": msg.mfrom, "to": msg.to, "hashtags": msg.hashtags, "msg": msg.text}
        self.factory.p.send_data(data)
