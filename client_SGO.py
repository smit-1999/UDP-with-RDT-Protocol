import socket,os,pickle,time,random,select
from packet import Packet
from datetime import datetime
from UDPsocket import MySocket
from clientHandler import Client



def main():
    myClient = Client()
    myClient.generateSeq()
    myClient.set_your_ip(("127.0.0.1", 9999))
    myClient.setTimeout(2)
    while True:
        reply = input("Client>")
        packet = myClient.createPacket(reply, myClient.getseq_num(), myClient.your_seq_num+1)
        myClient.sendPacket(packet)
        received = False
        while received == False:
            try : 
                data,ip = myClient.mySocket.recvfrom(1024)
                recvd_packet = pickle.loads(data)
                
                print('Received a packet having my seq no',recvd_packet.your_seq_num,'server seq no:',recvd_packet.seq_num)
                print('Expected seq no',myClient.expected_seq_num)
                if myClient.expected_seq_num == recvd_packet.your_seq_num:
                    print('Ack received from server')
                    received = True
                    myClient.handleAcks(recvd_packet)                    
            except socket.timeout :
                print("Retransmitting")
                myClient.handleTimeout(packet)                
                

main()



# try:
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# except socket.error:
#     print("Oops, something went wrong connecting the socket")
#     exit()

# seq_num = random.randrange(100000,900000,50)
# print(seq_num)

# server_socket = ("127.0.0.1", 9999)
# # sendThread = HandshakeSender(client_socket, (("127.0.0.1", 9999)), seq_num,"A1")
# # sendThread.start()

# # sendAckThread = 0

# # ackReceived = False
# # while ackReceived == False:
# #     data,ip = client_socket.recvfrom(1024)
# #     recvd_packet = pickle.loads(data)

# #     if recvd_packet is None:
# #         pass
# #     elif recvd_packet['payload'] == "A2":
# #         sendThread.kill()
       
# #         sendAckThread = HandshakeSender(client_socket, (("127.0.0.1", 9999)), seq_num,"B1")
# #         sendAckThread.start()
# #         ackReceived = True
# #         server_seq = recvd_packet['seq']
# #         print('Server seq no', server_seq)
        
# # time.sleep(3)
# # sendAckThread.kill()

# # print('Handshaking completed')
# server_seq = -1
# expected_seq_no = seq_num+1
# while True:
#     reply = input('Client>')

#     packet = Packet(seq_num,reply,'False',server_seq+1)
#     client_socket.sendto(pickle.dumps(packet),server_socket)    
#     client_socket.settimeout(2)
#     received = False
#     while received == False:
        
#         data=""
                
#         try : 
#             data,ip = client_socket.recvfrom(1024)
#             recvd_packet = pickle.loads(data)
            
#             print('Received a packet having my seq no',recvd_packet.your_seq_num,'server seq no:',recvd_packet.seq_num)
#             print('Expected seq no',expected_seq_no)
#             if expected_seq_no == recvd_packet.your_seq_num:
#                 print('ack received from server')
#                 received = True
#                 server_seq = recvd_packet.seq_num
#                 seq_num+=1
#                 expected_seq_no+=1
       
#         except socket.timeout :
#             print("retransmit")
#             client_socket.sendto(pickle.dumps(packet),(("127.0.0.1", 9999)))
        
        
        
        
        
#         # if data is None:
#         #     print("oh")
#         #     if (datetime.now() - timer).total_seconds() > 2:
#         #         print('Retransmit needed')
#         #         #retrnsmit needed
#         #         # client_socket.sendto(pickle.dumps(packet))
        
#         # else:
#         #     

