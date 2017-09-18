from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL


class RequestSentence(PacketType):

    DEFINITION_IDENTIFIER = "Zhiyuan.RequestSentence"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("clientID", UINT32)
    ]


class OriginalSentence(PacketType):

    DEFINITION_IDENTIFIER = "Zhiyuan.OriginalSentence"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("serverID", UINT32),
        ("ackClientID", UINT32),
        ("originalLanguageType", STRING),
        ("targetLanguageType", STRING),
        ("originalSentence", BUFFER)
    ]


class TranlatedSentence(PacketType):

    DEFINITION_IDENTIFIER = "Zhiyuan.TranlatedSentence"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("clientID", UINT32),
        ("ackServerID", UINT32),
        ("translatedSentence", BUFFER)

    ]


class Result(PacketType):

    DEFINITION_IDENTIFIER = "Zhiyuan.Result"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("serverID", UINT32),
        ("ackClientID", UINT32),
        ("passOrNot", BOOL),   # false stand for not pass, true stand for pass
        ("defaultAnswer", BUFFER)
    ]


print("Hi!")
