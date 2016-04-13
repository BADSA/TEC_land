from twisted.internet import protocol, reactor
from hostFactory import HostFactory


class Host:

    def __init__(self, ip, port):
        self.factory = HostFactory()
        self.routerIp = ip
        self.routerPort = port

    def connect(self):
        print "TEC-land host connecting to {0}:{1}".format(self.routerIp, self.routerPort)
        reactor.connectTCP(self.routerIp, self.routerPort, self.factory)

    def send_message(self, msg):
        data = {"from": msg.mfrom, "to": msg.to, "hashtags": msg.hashtags, "msg": msg.text}
        self.factory.p.sendData(data)
