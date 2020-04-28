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
        self.your_ip = 0
        self.your_seq_num = -1
    def createSocket(self):
        x = MySocket()
        x = x.create()
        return x

    def getMySocket(self):
        return self.mySocket

    def set_your_ip(self,ip):
        self.your_ip = ip

    def setTimeout(self,timeout):
        self.mySocket.settimeout(timeout)

    def getseq_num(self):
        return self.seq_num

    def generateSeq(self):
        seq = random.randrange(100000,999999,50)
        self.seq_num = seq
        self.expected_seq_num = self.seq_num+1
        return seq
    
    def createPacket(self, msg, mySeq , yourSeq):
        packet = Packet(mySeq,msg,False,yourSeq)
        return packet
    
    def sendPacket(self, packet):
        try:
            self.mySocket.sendto(pickle.dumps(packet), self.your_ip)
        except socket.error:
            print('error in sending packet')
    def sendMessage(self, receiverSocket,mySeq, yourSeq):
        try:
            packet = Packet(myseq,'data', False, yourSeq)
            packetSender = MySocket()
            packetSender.send_bytes(self.mySocket, receiverSocket, packet)
        except socket.error:
            print('Error in sending packets')

    def listen(self):
        data, ip = self.mySocket.recvfrom(1024)
        return data,ip
    def handleAcks(self,recvd_packet):
        self.your_seq_num = recvd_packet.seq_num
        self.seq_num+=1
        self.expected_seq_num+=1
    
    def handleTimeout(self, packet):
        self.mySocket.sendto(pickle.dumps(packet),self.your_ip)