import env
import sys
sys.path.append(env.infra_path)
import os
import mlog
import logging
mlog.configLoggers(['main', 'mq', 'parser'], env.logs_folder, env.debug_mode)

import json
import time
from mq import MQClient
from pcap_parser import parsePCAP
import keepalive
import base64
logger = logging.getLogger('main')

def onLivePCAP(req):
    try:
        logger.info('New live pcap file')
        filename = f"{req['origin']}-{req['time']}.pcap"
        filepath = os.path.join(env.pbak_folder, filename)
        with open(filepath, 'wb+') as fp:
            logger.debug('writing pcap file to folder')
            fp.write(base64.b64decode(req['data']))
        playFile(filename, req['origin'])
    except Exception as e:
        logger.error(str(e))

def onPlaybackRequest(req):
    logger.info('New playback request')
    if req['targetNetworkId'] == 'auto':
        target = None
    else:
        target = req['targetNetworkId']
    
    persist = True
    if 'persist' in req:
        persist = req['persist']
        
    playFile(req['file'], req['file'], targetNetworkId=target, persist=persist)

def playFile(filename, origin, targetNetworkId=None, persist=True):
    global mqc
    try:
        logger.info(f'Parsing file: {filename}')
        filepath = os.path.join(env.pbak_folder, filename)
        packets = parsePCAP(filepath, origin)

        packetsBuffer = {
            'time': time.time(),
            'origin': origin,
            'target': targetNetworkId,
            'numPackets': len(packets),
            'packets': packets,
            'persist': persist
        }
        logger.info(f'Parsed {len(packets)} packets from file')
        dmp_file = os.path.join(env.output_folder, f'pb-{filename}.json')
        with open(dmp_file, 'w') as f:
            json.dump(packetsBuffer,f,indent=4)
        mqc.publish('packetsBuffer', packetsBuffer)
        logger.info('pcap file parsed and published to processor')
    except Exception as e:
        logger.error(f'error processing pcap file: {e}')
    
try:
    mqc = MQClient(env)
    mqc.on_topic('playbackRequest', onPlaybackRequest)
    mqc.on_topic('livePCAP', onLivePCAP)
    keepalive.start(mqc, 'playback')
except KeyboardInterrupt:
    pass
except Exception as e:
    logger.fatal(str(e))