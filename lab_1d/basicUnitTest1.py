from playground.network.testing import MockTransportToStorageStream as MockTransport
from playground.asyncio_lib.testing import TestLoopEx
from playground.network.protocols.packets.vsocket_packets import VNICSocketOpenPacket, VNICSocketOpenResponsePacket, PacketType
from playground.network.protocols.packets.switching_packets import WirePacket
from playground.network.testing import MockTransportToProtocol

import io
import asyncio

from MyServerProtocol import MyServerProtocol
from MyClientProtocol import MyClientProtocol


def basicUnitTest():
    loop = asyncio.set_event_loop(TestLoopEx())

    serverProtocol = MyServerProtocol()
    clientProtocol = MyClientProtocol(loop)

# calling transportToServer’s write method will route the data directly to server’s data_received method
    #transportToServer = MockTransportToProtocol(serverProtocol)
    #transportToClient = MockTransportToProtocol(clientProtocol)

    transportToServer = MockTransportToProtocol(myProtocol=clientProtocol)
    transportToClient = MockTransportToProtocol(myProtocol=serverProtocol)

    # when setRemoteTransport is called, it writes data to the transport's protocol
    transportToServer.setRemoteTransport(transportToClient)
    transportToClient.setRemoteTransport(transportToServer)

    # serverProtocol.connection_made(transportToClient)
    # clientProtocol.connection_made(transportToServer)

    clientProtocol.connection_made(transportToServer)
    serverProtocol.connection_made(transportToClient)

    # try to send a pkt with clientID = 1
    clientProtocol.sendRequest(1)

    # try to send something not packet
    try:
        serverProtocol.data_received('Test')
    except TypeError:
        print(TypeError)


if __name__ == "__main__":
    basicUnitTest()
