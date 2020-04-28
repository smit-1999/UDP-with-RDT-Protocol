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
client_seq_init = 0
senderSock = 0
class receivePackets(Thread):
    def __init__(self,receiver_socket,msg,seqNo):
        Thread.__init__(self)
        global senderSock
        global client_seq_init
        self.msg = msg
        self.my_seq_num = seqNo
        self.mySocket = receiver_socket
        self.senderSocket = senderSock
        self.sender_seq = client_seq_init
        
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


class HandshakeSender(Thread):
    def __init__(self,seq,sender_socket,mySocket):
        Thread.__init__(self)
        self.seq_num = seq
        self.mySocket = mySocket
        self.senderSocket = sender_socket
        self.killed=False
    def run(self):
        while self.killed == False :
            print('Sending A2 to client')
            reply_packet={}
            reply_packet['payload'] = "A2"
            reply_packet['seq'] = self.seq_num
            self.mySocket.sendto(pickle.dumps(reply_packet),self.senderSocket)
            time.sleep(2)
    def kill(self):
        self.killed=True        
class HandshakeReceiver(Thread):
    def __init__(self,seq_num,mySocket):
        Thread.__init__(self)
        self.seq = seq_num
        self.mySocket = mySocket
        self.killed = False
    def run(self):
        while self.killed == False:
            data,ip = self.mySocket.recvfrom(1024)
            recvd_packet = pickle.loads(data)
            handshake_send = HandshakeSender(self.seq,ip,self.mySocket)
            global client_seq_init
            global senderSock
            if recvd_packet is None :
                pass
            elif recvd_packet["payload"] == "A1":                
                print('Received a packet from client with ip',ip)
                print('Client payload:',recvd_packet["payload"])
                client_seq_init = recvd_packet["seq"]
                senderSock = ip
                handshake_send.start()
                time.sleep(3)
                handshake_send.kill()
                self.killed = True
            # elif recvd_packet["payload"] == "B1":
            #     connection = True
            #     handshake_send.kill()
            #     print('handshake done,ready to receive msgs')
            #     self.killed = True