import socket,os,pickle,time,random
from packet import Packet
from UDPsocket import MySocket

#generate seq, sendPacket,retransmit,check timeout

class Client():
    def __init__(self):
        print('Creating handler for client')
        self.seq_num = 0        
        self.expected_seq_num = 0
        self.mySocket = self.createSocket()
        
    def createSocket():
        x = MySocket()
        x = x.create()
        return x

    def getMySocket():
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
    
    def sendMessage(self, receiverSocket,mySeq, yourSeq):
        try:
            packet = Packet(myseq,'data', False, yourSeq)
            packetSender = MySocket()
            packetSender.send_bytes(self.mySocket, receiverSocket, packet)
        except socket.error:
            print('Error in sending packets')