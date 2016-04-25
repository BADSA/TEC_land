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

from host import Host
from connectionFinder import ConnectionFinder


if __name__ == '__main__':
    """
    Point of start for a TEC-Land Host
    """

    conFinder = ConnectionFinder()

    print "Dynamic Binding"
    ip, port = conFinder.look_for_router()
    host = Host(ip, port)
    if ip is not None:
        host.start()
    else:
        print "No routers available"
