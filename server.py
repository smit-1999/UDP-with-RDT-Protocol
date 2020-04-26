import socket, pickle,time,logging,random,os
from packet import Packet
from serverThread import receivePackets, sendAcks
from threading import Thread

# set up the socket using local address
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(("", 9999))
print(f"Server started on localhost at port 9999.")
connection = False
status = ""
senderSock = 0

seq_num = random.randrange(100000,900000,50)
print(seq_num)
client_seq = 0

while connection != True:
    data,ip = socket.recvfrom(1024)
    if(data.decode(encoding="utf-8").strip()[:2] == "A1"):
        print("Obtained a client request,acknowledging connection")
        print("Client ip:",ip, "Data:",data)
        reply = "A2 seq:" + str(seq_num)
        client_seq = data.decode(encoding="utf-8").strip()[7:13]
        print(client_seq)
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