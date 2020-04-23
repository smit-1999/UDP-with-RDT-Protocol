import socket
import pickle,time
from packet import Packet
import os
from threading import Thread
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s RECEIVER [%(levelname)s] %(message)s',)
log = logging.getLogger()

# set up the socket using local address
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(("", 9999))
print(f"server started on localhost at port 9999")



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


connection = False
status = ""
senderSock = 0
while connection != True:
    data,ip = socket.recvfrom(1024)
    if(data.decode(encoding="utf-8").strip() == "A1"):
        print("Obtained a client request,acknowledging connection")
        print("client ip:",ip)
        reply = "A2"
        senderSock = ip
        reply=reply.encode()
        socket.sendto(reply,ip)
        time.sleep(1)
    elif (data.decode(encoding="utf-8").strip() == "B1"):
        connection = True
        print("Handshake done, ready to receive msgs")
        time.sleep(1)

pktReceiver =  receivePackets(socket, 0, 0)
ackSender = sendAcks(socket, senderSock)
pktReceiver.start()
ackSender.start()

pktReceiver.join()
ackSender.join()
# while 1:

#     # get the data sent to us
#     #data, ip = socket.recvfrom(1024)
    
#     data, ip = socket.recvfrom(4096)
#     recvd_Packet = pickle.loads(data)
#     # display
#     #print("Client> "+"{}: {}".format(ip, data.decode(encoding="utf-8").strip()))
#     print('Client ip : ',ip)
#     # print('Printing whole packet received from socket',data)
#     # print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))
#     # print('After pickling ',recvd_Packet)
    

#     print(recvd_Packet.seq_num, recvd_Packet.payload,recvd_Packet.isAck,recvd_Packet.msg.decode("utf-8"))
    

#     # echo back
#     reply = input(">")
#     reply = reply.encode()
#     msgpacket = Packet(0, 0, 0, reply)
#     data_string = pickle.dumps(msgpacket) 
#     socket.sendto(data_string, ip)