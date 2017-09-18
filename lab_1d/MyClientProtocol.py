import asyncio

import playground
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
from playground.network.common import PlaygroundAddress

from Mypacket import RequestSentence, OriginalSentence, TranlatedSentence, Result


class MyClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        # determining whether a protocol is connected by the status of its transport
        self.loop = loop
        self.transport = None
        self._deserializer = PacketType.Deserializer()

    def connection_made(self, transport):
        print("Connected to {}".format(transport.get_extra_info("peername")))
        self.transport = transport  # !!!!!!!!!!!!!!!!!!!
        print("Sentence requst sent")
        # self.transport.write(pkt1Bytes)
        # print(pkt1Bytes)

    def sendRequest(self, cID):
        requireSentencePkt = RequestSentence(clientID=cID)

        self.transport.write(requireSentencePkt.__serialize__())

    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            print("------------------------------")
            print(pkt)
            print("------------------------------")
            if isinstance(pkt, OriginalSentence):

                print("Receive a original sentence packet")
                print("serverID: {!r}".format(pkt.serverID))
                print("ackClientID: {!r}".format(pkt.ackClientID))
                print("originalSentence: {!r}".format(pkt.originalSentence))

                print("Send a translatedsentence packet")
                translatedPkt = TranlatedSentence(
                    clientID=pkt.ackClientID, ackServerID=pkt.serverID + 1, translatedSentence=b"wwwww")

                self.transport.write(translatedPkt.__serialize__())
            elif isinstance(pkt, Result):
                print("Receive a result packet")
                print("serverID: {!r}".format(pkt.serverID))
                print("ackClientID: {!r}".format(pkt.ackClientID))
                if pkt.passOrNot == True:
                    print("The answer is good!")
                else:
                    print("The answer is wrong!")
                print("defaultAnswer: {!r}".format(
                    pkt.defaultAnswer))

    def connection_lost(self, exc):
        self.transport = None
        print("Server Connection Lost because {}".format(exc))
        print("Stop the event loop")
        self.loop.stop()


loop = asyncio.get_event_loop()

# coro = loop.create_connection(
#     lambda: MyClientProtocol(loop), "127.0.0.1", 8001)
# loop.run_until_complete(coro)
# loop.run_forever()
# loop.close()

coro = playground.getConnector().create_playground_connection(
    lambda: MyClientProtocol(loop), '20174.1.1.1', 5555)
transport, protocol = loop.run_until_complete(coro)
print("Client Connected. Starting UI t:{}. p:{}".format(transport, protocol))

clientProtocol = MyClientProtocol(loop)
clientProtocol.sendRequest(1)

loop.run_forever()
loop.close()
