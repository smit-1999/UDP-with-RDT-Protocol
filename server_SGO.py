import socket,os,pickle,time,random
from packet import Packet
from serverHandler import Server

def main():
    myServer = Server()
    myServer.generateSeq()

    
    while True:
        data,ip = myServer.listen()
        recvd_packet = pickle.loads(data)
        myServer.set_your_ip(ip)
        print('Received a packet.Client ip : ', ip)
        print('Server seq no',recvd_packet.your_seq_num)
        print('Client seq no',recvd_packet.seq_num)
        print('Expected seq no',myServer.dictionary[ip][2])
                      

        if myServer.dictionary[ip][2] == recvd_packet.your_seq_num:
            #write to file
            print('Msg from client',recvd_packet.payload)
            myServer.handleExpectedPacket(recvd_packet, ip)
            
        elif myServer.dictionary[ip][2] > recvd_packet.your_seq_num:
            print('Duplicate packet detected.Packet payload : ', recvd_packet.payload)
            myServer.handleDuplicates(recvd_packet, ip)


        # if myServer.expected_seq_num == recvd_packet.your_seq_num:
        #     #write to file
        #     print('Msg from client',recvd_packet.payload)
        #     myServer.handleExpectedPacket(recvd_packet, ip)
            
        # elif myServer.expected_seq_num > recvd_packet.your_seq_num:
        #     print('Duplicate packet detected')
        #     myServer.handleDuplicates(recvd_packet, ip)
            

main()


connection = False
client_seq = 0
client_socket = 0


# handshake starts
# handshake_recv = HandshakeReceiver(seq_num,socket)
# handshake_recv.start()
# handshake_recv.join()
# print('Handshaking completed')
# time.sleep(2)

# while True:
#     data,ip = socket.recvfrom(1024)
#     recvd_packet = pickle.loads(data)
#     print('\nreceived packet server seq no',recvd_packet.your_seq_num)
#     print('received packet client seq no',recvd_packet.seq_num)
#     print('Expected seq no',expected_seq_num)
#     if recvd_packet is None:
#         pass
#     else:
#         if expected_seq_num == recvd_packet.your_seq_num:
#             print('msg from client',recvd_packet.payload,'My seq no in received packet:'
#             ,recvd_packet.your_seq_num)
#             seq_num+=1
#             replyPacket = Packet(seq_num ,'ack',True,recvd_packet.seq_num + 1)
#             expected_seq_num = seq_num + 1
#             socket.sendto(pickle.dumps(replyPacket),ip)
#         elif expected_seq_num > recvd_packet.your_seq_num:
#             print('Duplicate detected')
#             replyPacket = Packet(seq_num ,'ack',True, recvd_packet.seq_num + 1)
#             socket.sendto(pickle.dumps(replyPacket),ip)
#             # replyPacket = Packet(,'dup',True,)
#             # socket.sendto(pickle.dumps(replyPacket),ip)

   