

from twisted.words.protocols import irc

import json

class IRCClient(irc.IRCClient):
    nickname = "tecland"
    password = "tecland"

    def signedOn(self):
        # Called once the bot has connected to the IRC server
        self.join(self.factory.channel)
        print "Done"

    def send(self, msg):
        print msg, "IRCCLIENT"
        data = json.loads(msg)

        self.msg("#publico", "{0} says {1}".format(data["from"], data["message"]))

