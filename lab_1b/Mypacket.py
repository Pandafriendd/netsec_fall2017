'''
It is a Languages Translate Protocol

The IDs both on client and sever just like the IDs of TCP packets, 
to ensure the packets are in-order and to offer further support to reliable transmission

1. The client sends a request to sever for a sentence(Default as English) to translate into another language:
    * client sends RequestSentence(clientID) to sever
	
2. The sever responds by sending a English sentence(a sentence like "I love you" or a sentence from a poem) and its target language(like Chinese or French)
    * sever responds OriginalSentence(severID, ackClientID, originalLanguageType, targetLanguageType, originalSentence) to client
	
3. The client translates the original language into the target language
	* client sends TranlatedSentence(clientID, ackSeverID, translatedSentence) to sever
	
4. The sever checks whether the translated sentence has mistakes(grammar or meaning)and sends the result and a default answer  to client
	* Sever responds Result(severID, ackClientID, passOrNot, defaultAnswer)
'''



from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import UINT32, STRING, BUFFER, BOOL


class RequestSentence(PacketType):

    DEFINITION_IDENTIFIER = "lab1b.student_Zhiyuan.RequestSentence"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("clientID", UINT32)
    ]


class OriginalSentence(PacketType):

    DEFINITION_IDENTIFIER = "lab1b.student_Zhiyuan.OriginalSentence"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("severID", UINT32),
        ("ackClientID", UINT32),
        ("originalLanguageType", STRING),
        ("targetLanguageType", STRING),
        ("originalSentence", BUFFER)
    ]


class TranlatedSentence(PacketType):

    DEFINITION_IDENTIFIER = "lab1b.student_Zhiyuan.TranlatedSentence"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("clientID", UINT32),
        ("ackSeverID", UINT32),
        ("translatedSentence", BUFFER)

    ]


class Result(PacketType):

    DEFINITION_IDENTIFIER = "lab1b.student_Zhiyuan.Result"
    DEFINITION_VERSION = "1.0"

    FIELDS = [
        ("severID", UINT32),
        ("ackClientID", UINT32),
        ("passOrNot", BOOL),   # false stand for not pass, true stand for pass
        ("defaultAnswer", BUFFER)
    ]


print("Hi!")


def basicUnitTest():

    packet1 = RequestSentence()
    packet1.clientID = 1
    packet1Bytes = packet1.__serialize__()
    packet1a = RequestSentence.Deserialize(packet1Bytes)
    assert packet1 == packet1a
    if packet1 == packet1a:
        print("packet1 tested!")

    packet2 = OriginalSentence()
    packet2.severID = 1
    packet2.ackClientID = 2
    packet2.originalLanguageType = "English"
    packet2.targetLanguageType = "Chinese"
    packet2.originalSentence = b"I love you"
    packet2Bytes = packet2.__serialize__()
    packet2a = OriginalSentence.Deserialize(packet2Bytes)
    assert packet2 == packet2a
    if packet2 == packet2a:
        print("packet2 tested!")

    packet3 = TranlatedSentence()
    packet3.clientID = 2
    packet3.ackSeverID = 2
    packet3.translatedSentence = b"woaini"   # it is chinese yapin
    packet3Bytes = packet3.__serialize__()
    packet3a = TranlatedSentence.Deserialize(packet3Bytes)
    assert packet3 == packet3a
    if packet3 == packet3a:
        print("packet3 tested!")

    packet4 = Result()
    packet4.severID = 2
    packet4.ackClientID = 3
    packet4.passOrNot = True
    packet4.defaultAnswer = b"woaini"
    packet4Bytes = packet4.__serialize__()
    packet4a = Result.Deserialize(packet4Bytes)
    assert packet4 == packet4a
    if packet4 == packet4a:
        print("packet4 tested!")


if __name__ == "__main__":
    basicUnitTest()

