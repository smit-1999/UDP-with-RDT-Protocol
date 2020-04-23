import socket
import pickle,time 
from packet import Packet
from twh import ThreeWayHandshake
import hashlib
# create our udp socket
try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Oops, something went wrong connecting the socket")
    exit()

connection = False
while connection != True:
    print("Initiating handshake request")
    msg = "A1"
    msg = msg.encode()
    socket.sendto(msg, ("127.0.0.1", 9999))
    time.sleep(1)
    data,ip = socket.recvfrom(1024)
    if(data.decode(encoding="utf-8").strip() == "A2"):
        print("Ack obtained from server")
        msg = "B1"
        msg=msg.encode()
        time.sleep(1)
        socket.sendto(msg, ("127.0.0.1", 9999))
        connection = True
        print("handshake done, you can send mssgs")
        time.sleep(1)
time.sleep(1)

#begin chatting

while 1:
    message = input(">")
    print('input',message)
    # encode the message
    message = message.encode()

    try:
        # send the message
        msgpacket = Packet(0, 0, 0, message)
        print(msgpacket)        
        data_string = pickle.dumps(msgpacket)
        #print(data_string)
        
        socket.sendto(data_string, ("127.0.0.1", 9999))

        # output the response (if any)
        data, ip = socket.recvfrom(1024)
        recvd_Packet = pickle.loads(data)
        print('Server ip : ',ip)
        #print('Printing whole packet received from socket',data)
        #print('After pickling ',recvd_Packet)
        print(recvd_Packet.seq_num, recvd_Packet.payload,recvd_Packet.isAck,recvd_Packet.msg.decode("utf-8"))

    except socket.error:
        print("Error! {}".format(socket.error))
        exit()
