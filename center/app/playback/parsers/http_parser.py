import dpkt
from utils import *
name = 'http_parser'

def parseFunc(ts, eth):
    if isinstance(eth.data, dpkt.ip.IP):
        ip = eth.data
        if isinstance(ip.data, dpkt.tcp.TCP):
            tcp = ip.data
            parseHTTPPacket(ts, eth)

                
def parseHTTPPacket(ts, eth):
    try:
        ip  = eth.data
        tcp = ip.data
        request = dpkt.http.Request(tcp.data)
        src = getMACString(eth.src)
        description = 'http request from %s' % src
        print 'HTTP request: %s\n' % repr(request)
        
        return {
            'protocol': 'http',
            'layer': 7,
            'time': ts,
            'description': description,
            'source': {
                'mac': src,
                'ip': inet_to_str(ip.src)
            },
            'destination': {
                'ip': inet_to_str(ip.dst),
                'extraData': {
                    'HTTP request' : repr(request),
                    'HTTP sourceIP' : inet_to_str(ip.src)
                }
            }

        }
    except Exception as e:
        return None
