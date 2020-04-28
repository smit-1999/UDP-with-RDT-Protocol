import socket,os,pickle,time,random
from packet import Packet
from datetime import datetime
from ClientThread import HandshakeSender,HandshakeReceiver

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Oops, something went wrong connecting the socket")
    exit()

seq_num = random.randrange(100000,900000,50)
print(seq_num)

server_socket = ("127.0.0.1", 9999)
# sendThread = HandshakeSender(client_socket, (("127.0.0.1", 9999)), seq_num,"A1")
# sendThread.start()

# sendAckThread = 0

# ackReceived = False
# while ackReceived == False:
#     data,ip = client_socket.recvfrom(1024)
#     recvd_packet = pickle.loads(data)

#     if recvd_packet is None:
#         pass
#     elif recvd_packet['payload'] == "A2":
#         sendThread.kill()
       
#         sendAckThread = HandshakeSender(client_socket, (("127.0.0.1", 9999)), seq_num,"B1")
#         sendAckThread.start()
#         ackReceived = True
#         server_seq = recvd_packet['seq']
#         print('Server seq no', server_seq)
        
# time.sleep(3)
# sendAckThread.kill()

# print('Handshaking completed')
server_seq = -1
expected_seq_no = seq_num+1
while True:
    reply = input('Client>')
    packet = Packet(seq_num,reply,'False',server_seq+1)
    client_socket.sendto(pickle.dumps(packet),server_socket)
    timer = datetime.now()

    received = False
    while received == False:
        data,ip = client_socket.recvfrom(1024)
        recvd_packet = pickle.loads(data)
        if data is None:
            if datetime.now() - timer > 3:
                print('Retransmit needed')
                #retrnsmit needed
                # client_socket.sendto(pickle.dumps(packet))
        else:
            print('Not retransmitting.My seq no in packet:', recvd_packet.your_seq_num)
            if expected_seq_no == recvd_packet.your_seq_num:
                print('ack received from server')
                received = True
                server_seq = recvd_packet.seq_num
                seq_num+=1
                expected_seq_no+=1







