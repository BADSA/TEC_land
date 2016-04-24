
from twisted.cred import checkers, portal
from twisted.internet import reactor
from twisted.words import service

wordsRealm = service.InMemoryWordsRealm("localhost")
wordsRealm.createGroupOnRequest = True
wordsRealm.createUserOnRequest = True

checker = checkers.AllowAnonymousAccess()
checker2 = checkers.FilePasswordDB("passwords.txt")
portal = portal.Portal(wordsRealm, [checker, checker2])

reactor.listenTCP(6667, service.IRCFactory(wordsRealm, portal))
reactor.run()