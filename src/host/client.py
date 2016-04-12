from twisted.internet import reactor, protocol
import json


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.registerUser()

    def dataReceived(self, data):
        print data
        # self.transport.loseConnection()

    def registerUser(self):
        print "TEC-land network online..."
        username = raw_input("Please write an username to use: ")
        data = {"type": 'r', "username": username}
        self.transport.write(json.dumps(data))


class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed."
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost."
        reactor.stop()


reactor.connectTCP("localhost", 8000, EchoFactory())
reactor.run()
