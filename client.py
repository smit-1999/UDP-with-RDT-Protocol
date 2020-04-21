import socket
import pickle
from twh import ThreeWayHandshake
# create our udp socket
try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Oops, something went wrong connecting the socket")
    exit()

connection = False
while connection != True:
    msg = "A1"
    msg = msg.encode()
    socket.sendto(msg, ("127.0.0.1", 9999))
    data,ip = socket.recvfrom(1024)
    if(data.decode(encoding="utf-8").strip() == "A2"):
        msg = "B1"
        msg=msg.encode()
        socket.sendto(msg, ("127.0.0.1", 9999))
        connection = True
        print("handshake done, you can send mssgs")

while 1:
    message = input("> ")
    print('input',message)
    # encode the message
    message = message.encode()

    try:
        # send the message
        socket.sendto(message, ("127.0.0.1", 9999))

        # output the response (if any)
        data, ip = socket.recvfrom(1024)

        print("{}: {}".format(ip, data.decode()))

    except socket.error:
        print("Error! {}".format(socket.error))
        exit()
