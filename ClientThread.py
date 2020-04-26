import socket
import pickle,time
from packet import Packet
from datetime import datetime
import os
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s RECEIVER [%(levelname)s] %(message)s',)
log = logging.getLogger()

queue = []
timer = datetime.now()



class receivePackets(Thread):
    """
    This thread receives acks sent by the server.It listens on client socket for any incoming acks by the server.
    """

    def __init__(self,receiver_socket,msg):
        Thread.__init__(self)
        self.msg = msg
        self.mySocket = receiver_socket
        
    def run(self):
        log.info("Started to monitor packet receipt")
        
        while 1:
            data,ip = self.mySocket.recvfrom(4096)
            recvd_Packet = pickle.loads(data)
            print('Client ip: ',ip)
            recvd_seq_no = recvd_Packet['seq_num'] 
            print('Received ack  message with sequence number:', recvd_seq_no)
        print('Thread exited succesfully')

class windowHandler(Thread):
    def __init__(self,receiver_socket,sender_socket,seqnum,server_seqnum):
        Thread.__init__(self)
        self.receiverSocket = receiver_socket
        self.senderSocket = sender_socket
        self.my_seq_num = seqnum
        self.server_seq_num = server_seqnum
        
    def run(self):
        while 1:
            reply = input(">")
            reply = reply.encode()
            msgpacket = Packet(self.server_seq_num, 0, 0, reply)
            self.server_seq_num+=1
            data_string = pickle.dumps(msgpacket) 
            queue.append(data_string)
            #self.receiverSocket.sendto(data_string,self.senderSocket)

    def retransmit():
        for i in range (min(3, len(queue))):
            send_data = queue[i]
            self.receiverSocket.sendto(send_data,self.senderSocket)
            if(i == 0):
                timer = datetime.now()

class sendPackets(Thread):
    def __init__(self,receiver_socket,sender_socket):
        Thread.__init__(self)
        self.receiverSocket = receiver_socket
        self.senderSocket = sender_socket
    
    def run(self):
        while 1:
            while(len(queue)) :
                send_data = queue.pop(0)
                print(send_data)
                self.receiverSocket.sendto(send_data,self.senderSocket)

class timerclass(Thread) :
    def run(self):
        timer = datetime.now()
        while(1):
            if((datetime.now() - timer).total_seconds() > 1 and len(queue)>0 ) :
                windowHandler.retransmit()
                timer = datetime.now()
