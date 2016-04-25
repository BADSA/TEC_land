from twisted.internet import protocol, reactor
from ircClientFactory import IRCClientFactory
from listener import Listener


class IRCListenerFactory(protocol.Factory):
    def __init__(self, network, irc_port, channel):
        self.client = IRCClientFactory(channel)
        reactor.connectTCP(network, irc_port, self.client)

    def buildProtocol(self, addr):
        self.proto = Listener()
        self.proto.factory = self
        return self.proto