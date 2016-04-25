from twisted.internet import protocol
import json

class Listener(protocol.Protocol):

    def dataReceived(self, data):
        self.factory.client.send(data)
        self.transport.write(json.dumps({'msg': 'Message delivered successfully'}))
