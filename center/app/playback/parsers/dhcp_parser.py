import dpkt
from parsers.utils import *
name = 'dhcp_parser'
logger = None

def parseFunc(ts, eth):
    if isinstance(eth.data, dpkt.ip.IP):
        ip = eth.data
        if isinstance(ip.data, dpkt.udp.UDP):
            udp = ip.data
            if udp.sport == 67 or udp.sport == 68:
                return parseDHCPPacket(ts, eth)
                
def getDHCPOption(dhcp, opt_code):
    for opt in dhcp.opts:
        if opt[0] == opt_code:
            return opt[1]
    return None

def bytesToString(barr):
    return [str(barr[i]) for i in range(len(barr))]

def bytesToIntArray(barr):
    return [int(str(barr[i])) for i in range(len(barr))]

def parseDHCPPacket(ts, eth):
    try:
        ip  = eth.data
        udp = ip.data
        dh  = dpkt.dhcp.DHCP(udp.data)
        src = getMACString(eth.src)
        logger.debug('extracting dhcp finger print from packet')

        opt_53 = getDHCPOption(dh, 53)
        dhcp_type = int.from_bytes(opt_53, byteorder='big')
        opt_55 = getDHCPOption(dh, 55)
        dhcp_fp = bytesToIntArray(opt_55)
        hostname = getDHCPOption(dh, 12).decode("utf-8")
        VCI = getDHCPOption(dh, 60).decode("utf-8")
        print(hostname)
        if dhcp_type == 1:
            description = 'dhcp discover from %s' % src
        elif dhcp_type == 3:
            req_ip = getDHCPOption(dh, 50)
            description = 'dhcp request %s from %s' % (req_ip, src)
        else:
            return None
        
        return {
            'protocol': 'dhcp',
            'layer': 7,
            'time': ts,
            'description': description,
            'source': {
                'mac': src,
                'hostname': hostname,
                'extraData': {
                    'dhcpFingerPrint': dhcp_fp,
                    'VCI': VCI
                }
            }
        }
    except Exception as e:
        logger.error('dhcp parse exception: %s' % str(e))
        return None