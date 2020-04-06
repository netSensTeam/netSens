import binascii
import socket
def getMACString(mac_addr):
        """This function accepts a 12 hex digit string and converts it to a colon
            separated string"""
        mac_addr = binascii.hexlify(mac_addr)
        s = list()
        for i in range(6):  # mac_addr should always be 12 chars, we work in groups of 2 chars
                pair = mac_addr[2*i:2*i+2].decode("utf-8").upper()
                s.append(pair)
        r = ":".join(s)
        return r.upper()

def getIPString(ip_addr):
    return socket.inet_ntoa(ip_addr)