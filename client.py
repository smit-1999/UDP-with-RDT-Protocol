import socket,pickle,time,hashlib,os,logging,random
from packet import Packet
from ClientThread import receivePackets, windowHandler, sendPackets, timerclass
from twh import ThreeWayHandshake
from threading import Thread

# create our udp socket
try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Oops, something went wrong connecting the socket")
    exit()

connection = False
senderSock = 0
seq_num = random.randrange(100000,900000,50)
print(seq_num)
server_seq = 0


while connection != True:
    print("Initiating handshake request")
    handshake_packet = {}
    handshake_packet["payload"] = 'A1'
    handshake_packet["seq"] = seq_num
    socket.sendto(pickle.dumps(handshake_packet), (("127.0.0.1", 9999)))
    time.sleep(1)
    
    data,ip = socket.recvfrom(1024)
    recvd_packet = pickle.loads(data)
    
    if(recvd_packet['payload'] == "A2"):
        
        server_seq = recvd_packet['seq']
        print("Ack obtained from server.Server seq:", server_seq)
        time.sleep(1)
        reply_packet = {}
        reply_packet['payload'] = "B1"
        socket.sendto(pickle.dumps(reply_packet), ("127.0.0.1", 9999))
        connection = True
        print("handshake done, you can send mssgs")
        senderSock = ip
        time.sleep(1)
time.sleep(1)

#begin chatting
handler = windowHandler(socket, senderSock,seq_num,server_seq)
pktReceiver =  receivePackets(socket, 0)
pckSender = sendPackets(socket, senderSock)
timeout = timerclass(socket,senderSock)
pktReceiver.start()
handler.start()
pckSender.start()
timeout.start()

handler.join()
pktReceiver.join()
# while 1:
#     message = input(">")
#     print('input',message)
#     # encode the message
#     message = message.encode()

#     try:
#         # send the message
#         msgpacket = Packet(0, 0, 0, message)
#         print(msgpacket)        
#         data_string = pickle.dumps(msgpacket)
#         #print(data_string)
        
#         socket.sendto(data_string, ("127.0.0.1", 9999))

#         # output the response (if any)
#         data, ip = socket.recvfrom(1024)
#         recvd_Packet = pickle.loads(data)
#         print('Server ip : ',ip)
#         #print('Printing whole packet received from socket',data)
#         #print('After pickling ',recvd_Packet)
#         print(recvd_Packet.seq_num, recvd_Packet.payload,recvd_Packet.isAck,recvd_Packet.msg.decode("utf-8"))

#     except socket.error:
#         print("Error! {}".format(socket.error))
#         exit()
