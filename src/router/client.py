from time import sleep
from twisted.internet import reactor, protocol, defer
import json
class RouterClientConnection(protocol.Protocol):

    def connectionMade(self):
        data = {"type": 'q'}
        self.transport.write(json.dumps(data))

    def dataReceived(self, data):
        response = {"conn": data,  "client": str(self.transport.getPeer())}
        self.factory.response.append(response)
        self.transport.loseConnection()


class RouterClient(protocol.ClientFactory):

    def buildProtocol(self, addr):
        p = RouterClientConnection()
        p.factory = self
        return p

    def get_response(self):
        return self.response
