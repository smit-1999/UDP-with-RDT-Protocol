import socket, pickle,time,logging,random,os
from packet import Packet
from serverThread import receivePackets, sendAcks, sendPackets
from threading import Thread

# set up the socket using local address
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(("", 9999))
print(f"Server started on localhost at port 9999.")
connection = False
status = ""
senderSock = 0                                      #client socket details

seq_num = random.randrange(100000,900000,50)        #server sequence number
print(seq_num)
client_seq = 0                                      #client seq number

while connection != True:
    #receive the data sent
    data,ip = socket.recvfrom(1024)
    recvd_packet = pickle.loads(data)
    
    
    if(recvd_packet['payload'] == "A1"):
        print("Obtained a client request,acknowledging connection")        
        client_seq = recvd_packet['seq']
        print('Client seq no is:',client_seq,"\nClient ip:",ip)
        
        senderSock = ip                             #client socket details
        reply_packet = {}
        reply_packet['payload'] = "A2"; reply_packet['seq'] = seq_num
        socket.sendto(pickle.dumps(reply_packet),ip) 
        time.sleep(1)
    elif (recvd_packet['payload'] == "B1"):
        connection = True
        print("Handshake done, ready to receive msgs")
        time.sleep(1)

pktReceiver =  receivePackets(socket,senderSock, 0, seq_num, client_seq) #thread to receive packets and send acks
pktReceiver.start()
pktReceiver.join()

