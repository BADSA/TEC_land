from twisted.internet import protocol


class Listener(protocol.Protocol):

    def dataReceived(self, data):
        print data, "LISTENER"
        self.factory.client.send(data)
        self.transport.write("{'msg':'ok'}")