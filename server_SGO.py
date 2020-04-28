import socket,os,pickle,time,random
from packet import Packet
from serverThread import HandshakeReceiver


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

    if recvd_packet is None:
        pass
    else:
        if expected_seq_num == recvd_packet.your_seq_num:
            print('msg from client',recvd_packet.payload,'My seq no in received packet:'
            ,recvd_packet.your_seq_num)
            replyPacket = Packet(seq_num ,'ack',True,recvd_packet.seq_num + 1)
            expected_seq_num = seq_num + 1
            socket.sendto(pickle.dumps(replyPacket),ip)


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
