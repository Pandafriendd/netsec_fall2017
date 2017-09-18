import asyncio

import playground
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL
from playground.network.common import PlaygroundAddress
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

from Mypacket import RequestSentence, OriginalSentence, TranlatedSentence, Result
from PassThrough1 import PassThroughProtocol1
from PassThrough2 import PassThroughProtocol2


class MyServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self._deserializer = PacketType.Deserializer()

    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        print("Connection from {}".format(peername))
        self.transport = transport

    def data_received(self, data):
        self._deserializer.update(data)
        for pkt in self._deserializer.nextPackets():
            print("------------------------------")
            print(pkt)
            print("------------------------------")
            # pkt will ALWAYS be defined (never None). And it will already be the right class

            if isinstance(pkt, RequestSentence):
                print("It's a RequestSentence packet")
                print("clientID: {!r}".format(pkt.clientID))

                print("Send a original sentence")
                responsePkt = OriginalSentence(serverID=50, ackClientID=pkt.clientID + 1, originalLanguageType="English",
                                               targetLanguageType="Chinese", originalSentence=b"I love you")

                self.transport.write(responsePkt.__serialize__())
            elif isinstance(pkt, TranlatedSentence):
                print("It's a TranslatedSentence packet")
                print("clientID: {!r}".format(pkt.clientID))
                print("ackServerID: {!r}".format(pkt.ackServerID))
                print("translatedSentence: {!r}".format(
                    pkt.translatedSentence))

                print("Send a result")
                resultPkt = Result(serverID=pkt.ackServerID,
                                   ackClientID=pkt.clientID + 1, defaultAnswer=b"woaini", passOrNot=True)
                if pkt.translatedSentence == resultPkt.defaultAnswer:
                    resultPkt.passOrNot = True
                else:
                    resultPkt.passOrNot = False

                self.transport.write(resultPkt.__serialize__())

            else:
                raise TypeError("It is not a correct packet!")

    def connection_lost(self, reason=None):
        print("Lost connection to client.")


loop = asyncio.get_event_loop()

# to construct a new protocol instance for each incoming connection
# for a server, there will be multiple connections per port

# coro = loop.create_server(lambda: MyServerProtocol(), "127.0.0.1", 8001)
# server = loop.run_until_complete(coro)

# Server requests until Ctrl+C is pressd
# print('Serving on {}'.format(server.sockets[0].getsockname()))
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass

# Close the server
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()

f = StackingProtocolFactory(
    lambda: PassThroughProtocol1(), lambda: PassThroughProtocol2())
ptConnector = playground.Connector(protocolStack=f)
playground.setConnector("passthrough", ptConnector)

coro = playground.getConnector("passthrough").create_playground_server(
    lambda: MyServerProtocol(), 5555)
server = loop.run_until_complete(coro)
print("Server Started(pt)")
loop.run_forever()
loop.close()


# coro = playground.getConnector().create_playground_server(
#     lambda: MyServerProtocol(), 5555)
#server = loop.run_until_complete(coro)
#print("Server Started at {}".format(server.sockets[0].gethostname()))
# loop.run_forever()
# loop.close()
