import env
import sys
sys.path.extend(['models','entities',env.infra_path])

import logging
import signal
import keepalive
from network_lock import NetworkLock
from mq import MQClient
from db import DBClient

import mlog
import os
import processorsManager

mlog.configLoggers(['main', 'network', 'proc', 'mq', 'db', 'model'], env.logs_folder, env.debug_mode)
logger = logging.getLogger('main')

try:
    mqc = MQClient(env)
    dbc = DBClient(env)
    nlock = NetworkLock(dbc)
    processorsManager.loadProcessors(mqc, dbc, nlock, env)
    logger.info('Networker is up')
    keepalive.start(mqc, 'networker')
except KeyboardInterrupt:
    logger.info('Networker process was closed by user')
except Exception as e:
    logger.fatal(str(e))