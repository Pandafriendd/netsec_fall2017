import playground
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory

# inherit from StackingProtocol to make a stacking protocol


class PassThroughProtocol1(StackingProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        print("PassThroughLayer1 connection made")
        self.higherProtocol().connection_made(StackingTransport(self.transport))

    def data_received(self, data):
        print("PassThroughLayer1 received data")
        self.higherProtocol().data_received(data)

    def connection_lost(self, reason):
        print("PassThroughLayer1 connection lost")
        self.higherProtocol().connnection_lost(reason)
