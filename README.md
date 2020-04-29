# UDP-with-RDT-Protocol

This is a part of the Computer Networks Assignment at BITS Pilani. We are planning to build an application layer protocol which ensures retransmissions,acks,seq numbers while sending packets through UDP protocol.

This assignment was done by

1)Smit Shah : 2017A7PS0080H
2)Shikhar Dhawale : 2017A7PS0049H
3)Anish Walia
4)Anish Dey
5)Aniruddh Gupta

The application consists of a server and client.The client sends message to a client,which the server writes to a file.Multiple clients can send message to the server.

The server file can be run by:
`python3 server_SGO.py`

This starts the server file,which listens on port 9999.
Each client is run as a thread in another terminal,and can be run by
`python3 client_SGO.py`

These packets get written to
_client_messages/<clientip_port>.txt_
It contains the data sent by the client to the server.

### Dependencies

For running these files you will need to have these python libraries installed :

1.  _socket_
2.  _pickle_
3.  _time_
4.  _random_
5.  _csv_
6.  _threading_

### Network Simulation

Using the _netem_ tool,we can simulate conditions like packet loss,packet delays and packet corruption.We can insert rules in our Ubuntu terminal to simulate the conditions.

The _lo_ interface refers to _localhost_

**To view all the rules:**
`sudo tc qdisc show dev lo`

**To delete all the rules for an interface:**
`sudo tc qdisc del dev lo root`

**To simulate packet loss :**
`sudo tc qdisc add dev lo root netem loss 0.1%`
This causes 1/10th of a percent (i.e 1 out of 1000) packets to be randomly dropped.The _lo_ can be changed to interface on which you want to test.

**To simulate packet reordering :**
`sudo tc qdisc add dev lo root netem gap 3 delay 1000ms reorder 50%`
This causes with a 50%probability for every 3rd packet to be sent first and the remaining packets to have a delay of 1000ms.

**To corrupt packets**
`sudo tc qdisc add dev lo root netem corrupt 0.1%`

**To add fixed delay to all packets**
`sudotc qdisc add dev lo root netem delay 100ms`
