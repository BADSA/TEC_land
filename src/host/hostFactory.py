from twisted.internet import protocol
from chatClient import ChatClient


class HostFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ChatClient()

    def __init__(self, r_file):
        pass

    def buildProtocol(self, addr):
        return ChatClient()
