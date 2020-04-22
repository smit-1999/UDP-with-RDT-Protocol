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
