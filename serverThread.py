import socket
import pickle,time
from packet import Packet
import os
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s RECEIVER [%(levelname)s] %(message)s',)
log = logging.getLogger()

expected_seq_num = 0

class receivePackets(Thread):
    def __init__(self,receiver_socket,sender_socket,msg,seqNo,sender_seqno):
        Thread.__init__(self)
        self.msg = msg
        self.my_seq_num = seqNo
        self.mySocket = receiver_socket
        self.senderSocket = sender_socket
        self.sender_seq = sender_seqno
        
    def run(self):
        log.info("Started to monitor packet receipt")
        expected_seq_num = self.my_seq_num
        while 1:
            """
            Listen to the socket port,if there's an incoming packet which matches the seq_num,pass it to the application layer
            If not,send an ack msg having the seq_num of the last received in-order packet
            """
            data,ip = self.mySocket.recvfrom(4096)
            recvd_Packet = pickle.loads(data)
            print('Client ip: ',ip,"sent data : ", recvd_Packet.msg)
            
            if(recvd_Packet.seq_num == expected_seq_num):
                recvdMsg = recvd_Packet.msg.decode("utf-8") 
                
                #writeToFile(recvdMsg)

                
                ack_msg = {}
                print('Sender seq no',self.sender_seq)
                ack_msg['seq_num'] = self.sender_seq
                ack_msg = pickle.dumps(ack_msg)
                self.mySocket.sendto(ack_msg,self.senderSocket)     #send Ack message
                
                expected_seq_num+=1                                 #Increment seq number 
                self.sender_seq+=1                                  #increment seq number of ack packet
                
                
            else:
                print('HI')
                ack_msg = {}
                ack_msg['seq_num'] = self.sender_seq
                ack_msg = pickle.dumps(ack_msg)
                self.mySocket.sendto(ack_msg,self.senderSocket)
                
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
            queue.append(data_string)
            #self.receiverSocket.sendto(data_string,self.senderSocket)

class sendPackets(Thread):
    def __init__(self,receiver_socket,sender_socket):
        Thread.__init__(self)
        self.receiverSocket = receiver_socket
        self.senderSocket = sender_socket
    
    def run(self):
        while 1:
            while(len(queue)) :
                send_data = queue.pop(0)
                self.receiverSocket.sendto(send_data,self.senderSocket)