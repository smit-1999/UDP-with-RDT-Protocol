import hashlib

class Packet : 
    seq_num = 0
    payload = 0
    checksum =0
    isAck = 0
    msg = ""

    def __init__(self, seq_num, payload, isAck, msg): 
        self.seq_num = seq_num
        self.payload = payload
        self.isAck = isAck
        self.msg = msg

    def __eq__(self, other):
        return self.seq_num == other.seq_num and self.payload == other.payload  and self.isAck == other.isAck and self.msg == other.msg

    def __hash__(self):
        
        return hash((self.seq_num, self.payload, self.isAck , self.msg))

    def setChecksum(self,val):
        self.checksum = val
    
