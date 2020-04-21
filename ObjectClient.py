import socket
import pickle
from twh import ThreeWayHandshake
# from gc import enable
from time import sleep
SERVER_ADDRES = "127.0.0.1"
SERVER_PORT = 5000


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (SERVER_ADDRES, SERVER_PORT)
    conn1 = ThreeWayHandshake()
    #print("before", conn1)
    sock.connect(address)
    conn1.Connection()
    while conn1.connected != True:
        print("client side:", conn1)
        sock.sendall(pickle.dumps(conn1))
        if conn1.connected == True:
            break
        del conn1
        data = sock.recv(4096)
        sleep(1)
        conn1 = pickle.loads(data)
        del data
        print("client side after response:", conn1)
        conn1.Connection()
        sleep(3)

    print("done.") if conn1.connected == True else print("not done")
    while 1:
        message = input("> ")
        print('input',message)
        # encode the message
        message = message.encode()

        try:
            # send the message
            sock.sendto(message, ("127.0.0.1", 5000))

            # output the response (if any)
            data, ip = sock.recvfrom(1024)

            print("{}: {}".format(ip, data.decode()))

        except socket.error:
            print("Error! {}".format(socket.error))
            exit()

# enable()
main()
