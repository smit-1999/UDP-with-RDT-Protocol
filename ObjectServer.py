import socket
import pickle
from twh import ThreeWayHandshake
# from gc import enable
from time import sleep
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 5000
hanler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (SERVER_ADDRESS, SERVER_PORT)
print(f"server {SERVER_ADDRESS} at port {SERVER_PORT}")
hanler.bind(address)
hanler.listen(1)


def main():
    con = (hanler.accept()[0])
    connection = False
    while connection != True:
        print("wating for connection")
        # sleep(3)
        data = con.recv(4096)
        obj = pickle.loads(data)
        del data
        print("recieved.")
        obj.Connection()
        print("server side:", obj)
        con.sendall(pickle.dumps(obj))
        connection = obj.IsConnected()
    print("3-way done!!!")
    
    hanler.bind(address)
    hanler.listen(1)

    while 1:
          
        # get the data sent to us
        data, ip = hanler.recvfrom(1024)

        # display
        print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))

        # echo back
        data = input("Server >")
        data = data.encode() 
        hanler.sendto(data, ip)

    con.close()
# enable()
main()
