import socket
import pickle
from twh import ThreeWayHandshake
# from gc import enable
from time import sleep
SERVER_ADDRESS = ""
SERVER_PORT = 5000
hanler = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (SERVER_ADDRESS, SERVER_PORT)
print(f"server {SERVER_ADDRESS} at port {SERVER_PORT}")
hanler.bind(address)

def main():
    # con = (hanler.accept()[0])
    connection = False
    status = ""
    while connection != True:
        print("wating for connection")
                    
        obj.Connection()
        print("server side:", obj)
        con.sendall(pickle.dumps(obj))
        connection = obj.IsConnected()
    print("3-way done!!!")

   

    while 1:
          
        # get the data sent to us
        data, ip = con.recvfrom(1024)

        # display
        print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))

        # echo back
        data = input("Server >")
        data = data.encode()
        con.sendto(data, ip)

    con.close()
# enable()
main()