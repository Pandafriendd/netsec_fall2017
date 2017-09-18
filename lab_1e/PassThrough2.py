import playground
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory


class PassThroughProtocol2(StackingProtocol):
    def __init__(self):
        super().__init__

    def connection_made(self, transport):
        self.transport = transport
        print("PassThroughLayer2 connection made")
        self.higherProtocol().connection_made(self.trasnport)

    def data_received(self, data):
        print("PassThroughLayer2 received data")
        self.higherProtocol().data_received(data)

    def connection_lost(self, reason):
        print("PassThroughLayer2 connection lost")
        self.higherProtocol().connnection_lost(reason)
