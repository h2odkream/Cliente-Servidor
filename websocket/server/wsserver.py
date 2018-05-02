#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import protocol, reactor, endpoints
from txws import WebSocketFactory


class ClientProtocol(protocol.Protocol):

    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, data):
        self.factory.sendMessage(data)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def connectionMade(self):
        self.factory.clients.add(self)


class ClientFactory(protocol.Factory):

    def __init__(self):
        self.clients = set()

    def buildProtocol(self, addr):
        return ClientProtocol(self)

    def sendMessage(self, message):
        for client in self.clients:
            client.transport.write(message)


endpoints.serverFromString(reactor, "tcp:9998").listen(
    WebSocketFactory(ClientFactory()))
reactor.run()
