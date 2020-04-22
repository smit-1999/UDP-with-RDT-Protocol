import socket,time

# set up the socket using local address
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(("", 9999))
print(f"server started on localhost at port 9999")

connection = False
status = ""
while connection != True:
    data,ip = socket.recvfrom(1024)
    if(data.decode(encoding="utf-8").strip() == "A1"):
        print("Obtained a client request,acknowledging connection")
        reply = "A2"
        reply=reply.encode()
        socket.sendto(reply,ip)
        time.sleep(1)
    elif (data.decode(encoding="utf-8").strip() == "B1"):
        connection = True
        print("Handshake done, ready to receive msgs")
        time.sleep(1)
    

while 1:

    # get the data sent to us
    data, ip = socket.recvfrom(1024)

    # display
    print("Client> "+"{}: {}".format(ip, data.decode(encoding="utf-8").strip()))

    # echo back
    data = input(">")
    data = data.encode() 
    socket.sendto(data, ip)