import threading
import time
import logging
import logging
import mlog
from importlib import import_module
import os
import ns_utils
logger = logging.getLogger('plugin')

def load(mqc, dbc, env):
    for pluginName in ns_utils.getPackages('plugins'):
        try:
            logger.info('Loading plugin %s', pluginName)
            mdl = import_module('plugins.' + pluginName)
            mlog.configLoggers([mdl.name], env.logs_folder, env.debug_mode)
            Plugin(mdl, mqc, dbc)
        except Exception as e:
            logger.error('Failed to load plugin %s: %s', pluginName, str(e))
            
class Plugin:
    def __init__(self, module, mqc, dbc):
        self.logger = logging.getLogger(module.name)
        self.module = module
        self.mqc = mqc
        self.dbc = dbc
        self.mqc.on_topic('plugin-device-%s' % self.module.uuid, self.manual_process_device)
        self.mqc.on_topic('device', self.process_device)
        
        self.module.setLogger(self.logger)
        thread = threading.Thread(target=self.publish)
        thread.daemon = True
        thread.start()
    def publish(self):
        while True:
            self.desc = {
                'uuid': self.module.uuid,
                'name': self.module.name,
                'level': self.module.level,
                'lastUpdateTime': time.time()
            }
            self.dbc.db.plugins.update_one(
                {'uuid': self.module.uuid},
                {'$set': self.desc}, 
                upsert=True
            )
            time.sleep(10)

    def process_device(self, device, manual=False):
        extraData = self.module.processDevice(device, manual)
        
        if extraData:
            self.mqc.publish('deviceExtraData', {
                'networkUUID': device['networkId'],
                'deviceUUID': device['uuid'],
                'extraData': extraData
            })
    
    def manual_process_device(self, device):
        self.logger.info('manual device process')
        self.process_device(device, manual=True)