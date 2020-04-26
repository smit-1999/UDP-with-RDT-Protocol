# UDP-with-RDT-Protocol
This is a part of the Computer Networks Assignment at BITS Pilani. We are planning to build an application layer protocol which ensures retransmissions,acks,seq numbers while sending packets through UDP protocol.


To view all the rules:
sudo  tc qdisc show  dev lo

To delete all the rules for an interface:
sudo tc qdisc del dev lo root


To simulate network conditions for packet loss :

Use the command : sudo tc qdisc add dev lo root netem loss 50%

The lo can be changed to interface on which you want to test.50% is the loss probability,i.e. out of 100,50 packets will be lost.

To simulate packet reordering : 
Use : sudo tc qdisc add dev lo root netem gap 3 delay 1000ms reorder 50%

This causes with a 50%probability for every 3rd packet to be sent first and the remaining packets to have a delay of 1000ms.


