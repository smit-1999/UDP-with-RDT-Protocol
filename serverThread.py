import socket
import pickle,time
from packet import Packet
import os
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s RECEIVER [%(levelname)s] %(message)s',)
log = logging.getLogger()

class receivePackets(Thread):
    def __init__(self,receiver_socket,msg,seqNo):
        Thread.__init__(self)
        self.msg = msg
        self.seqNo = seqNo
        self.receiverSocket = receiver_socket
    def run(self):
        log.info("Started to monitor packet receipt")
        
        while 1:
            data,ip = self.receiverSocket.recvfrom(4096)
            recvd_Packet = pickle.loads(data)
            print('Client ip: ',ip)
            recvdMsg = recvd_Packet.msg.decode("utf-8") 
            print('Received message:', recvdMsg)
            if(recvdMsg == "quit"):
                print('Exiting receiver thread on server side')
                break
        print('Thread exited succesfully')

class sendAcks(Thread):
    def __init__(self,receiver_socket,sender_socket):
        Thread.__init__(self)
        self.receiverSocket = receiver_socket
        self.senderSocket = sender_socket
    def run(self):
        while 1:
            reply = input(">")
            reply = reply.encode()
            msgpacket = Packet(0, 0, 0, reply)
            data_string = pickle.dumps(msgpacket) 
            self.receiverSocket.sendto(data_string,self.senderSocket)