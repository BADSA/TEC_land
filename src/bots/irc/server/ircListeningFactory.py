
from twisted.internet import protocol, reactor
from listener import Listener
from bots.irc.client.ircClientFactory import IRCClientFactory

# Factory that allows to handle the
# incoming messages

class IRCListenerFactory(protocol.Factory):
    def __init__(self, network, irc_port, channel):
        self.client = IRCClientFactory(channel)
        reactor.connectTCP(network, irc_port, self.client)

    def buildProtocol(self, addr):
        self.proto = Listener()
        self.proto.factory = self
        return self.proto