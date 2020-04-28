import socket,os,pickle,time,random
from packet import Packet
from UDPsocket import MySocket

#encapsulate payload,adds seq number ack payload:basically use Packet class
#
class Server():
    def __init__(self):
        print('Creating handler for server')
        self.seq_num = 0        
        self.expected_seq_num = 0
        self.mySocket = self.createSocket()
        print(self.mySocket)        
        
    def createSocket(self):
        x = MySocket()
        newSocket = x.create()
        boundSocket = x.bind(newSocket, 9999)
        return boundSocket

    def getMySocket(self):
        return self.mySocket

    def getseq_num(self):
        return self.seq_num

    def generateSeq(self):
        seq = random.randrange(100000,999999,50)
        self.seq_num = seq
        return seq

    def createPacket(self, msg, mySeq , yourSeq):        
        packet = Packet(mySeq,msg,True,yourSeq)
        return packet
    
    def sendAcks(self, receiverSocket , mySeq, yourSeq):
        packet = Packet(myseq, 'ack', True, yourSeq)
        ackSender = MySocket()
        ackSender.send_bytes(self.mySocket, receiverSocket, packet)
    
    def listen(self):
        data, ip = self.mySocket.recvfrom(1024)
        return data,ip
    