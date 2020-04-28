import socket,os,pickle,time,random
from packet import Packet
from serverHandler import Server

def main():
    myServer = Server()
    myServer.generateSeq()

    
    while True:
        data,ip = myServer.listen()
        recvd_packet = pickle.loads(data)

        print('\nreceived packet server seq no',recvd_packet.your_seq_num)
        print('received packet client seq no',recvd_packet.seq_num)
        print('Expected seq no',myServer.expected_seq_num)
        
        

        if myServer.expected_seq_num == recvd_packet.your_seq_num:
            #write to file
            print('msg from client',recvd_packet.payload)
            myServer.seq_num+=1
            replyPacket = Packet(myServer.seq_num ,'ack',True,recvd_packet.seq_num + 1)
            myServer.expected_seq_num = myServer.seq_num + 1
            myServer.mySocket.sendto(pickle.dumps(replyPacket),ip)
        elif myServer.expected_seq_num > recvd_packet.your_seq_num:
            print('Duplicate detected')
            replyPacket = Packet(myServer.seq_num ,'ack',True, recvd_packet.seq_num + 1)
            myServer.mySocket.sendto(pickle.dumps(replyPacket),ip)

main()

seq_num = random.randrange(100000,900000,50)        #server sequence number
print(seq_num)


socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(("", 9999))
print(f"Server started on localhost at port 9999.")

connection = False
client_seq = 0
client_socket = 0
expected_seq_num = 0

# handshake starts
# handshake_recv = HandshakeReceiver(seq_num,socket)
# handshake_recv.start()
# handshake_recv.join()
# print('Handshaking completed')
# time.sleep(2)

while True:
    data,ip = socket.recvfrom(1024)
    recvd_packet = pickle.loads(data)
    print('\nreceived packet server seq no',recvd_packet.your_seq_num)
    print('received packet client seq no',recvd_packet.seq_num)
    print('Expected seq no',expected_seq_num)
    if recvd_packet is None:
        pass
    else:
        if expected_seq_num == recvd_packet.your_seq_num:
            print('msg from client',recvd_packet.payload,'My seq no in received packet:'
            ,recvd_packet.your_seq_num)
            seq_num+=1
            replyPacket = Packet(seq_num ,'ack',True,recvd_packet.seq_num + 1)
            expected_seq_num = seq_num + 1
            socket.sendto(pickle.dumps(replyPacket),ip)
        elif expected_seq_num > recvd_packet.your_seq_num:
            print('Duplicate detected')
            replyPacket = Packet(seq_num ,'ack',True, recvd_packet.seq_num + 1)
            socket.sendto(pickle.dumps(replyPacket),ip)
            # replyPacket = Packet(,'dup',True,)

            # socket.sendto(pickle.dumps(replyPacket),ip)

    # while connection == False:
    #     data,ip = socket.recvfrom(1024)
    #     recvd_packet = pickle.loads(data)
    #     if recvd_packet is None:
    #         pass
    #     elif recvd_packet["payload"] == "A1":
    #         client_socket = ip
    #         client_seq = recvd_packet["seq"]
    #     elif recvd_packet["payload"] == "B1":
    #         connection = True
