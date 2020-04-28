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

expected_ack_no = 0
received_seq_no = 0 
window_size = 5
nextseqnum = 0
base = 0
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
        global expected_ack_no,nextseqnum
        while 1:
            data,ip = self.mySocket.recvfrom(4096)
            recvd_Packet = pickle.loads(data)
            print('Client ip: ',ip)
            recvd_seq_no = recvd_Packet['seq_num'] 
            received_seq_no = recvd_seq_no

            if(received_seq_no == expected_ack_no):
                expected_ack_no+=1
                if len(queue)>0:
                    queue.pop(0)
                timer = datetime.now()
                nextseqnum-=1
            elif(received_seq_no > expected_ack_no):
                diff = 0
                
                while(diff != (received_seq_no-expected_ack_no)):
                    if len(queue) == 0:
                        break
                    else :
                        queue.pop(0)
                        diff+=1
                expected_ack_no = received_seq_no + 1
                nextseqnum-=diff
                timer=datetime.now()
            print('Received ack  message with sequence number:', recvd_seq_no)
        print('Thread exited succesfully')

class windowHandler(Thread):
    def __init__(self,receiver_socket,sender_socket,seqnum,server_seqnum):
        Thread.__init__(self)
        self.receiverSocket = receiver_socket
        self.senderSocket = sender_socket
        self.my_seq_num = seqnum
        self.server_seq_num = server_seqnum
        expected_ack_no = seqnum
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
        for i in range (min(window_size, len(queue))):
            send_data = queue[i]
            self.receiverSocket.sendto(send_data,self.senderSocket)
            if(i == 0):
                timer = datetime.now()

class sendPackets(Thread):
    def __init__(self,receiver_socket,sender_socket):
        Thread.__init__(self)
        self.mySocket = receiver_socket
        self.senderSocket = sender_socket
    
    def run(self):        
        global nextseqnum 
        global base
        global window_size
        while (1):           
            while(len(queue)) :
                
                if(len(queue) > 0 and nextseqnum<window_size):
                    for i in range(nextseqnum,window_size):                    
                        if(i < len(queue)):
                            self.mySocket.sendto(queue[i], self.senderSocket)
                            nextseqnum+=1
                    if len(queue) == 0:
                        break

                # send_data = queue.pop(0)
                # print(send_data)
                # self.receiverSocket.sendto(send_data,self.senderSocket)

class timerclass(Thread) :
    def __init__(self,mySocket,senderSock):
        Thread.__init__(self)
        self.receiverSocket = mySocket
        self.senderSocket = senderSock
    def run(self):
        timer = datetime.now()
        while(1):
            if((datetime.now() - timer).total_seconds() > 2 and len(queue)>0 ) :
                self.retransmit()
                timer = datetime.now()

    def retransmit(self):
        for i in range (min(window_size, len(queue))):
            #list index out of range
            send_data = queue[i]
            self.receiverSocket.sendto(send_data,self.senderSocket)
            if(i == 0):
                timer = datetime.now()