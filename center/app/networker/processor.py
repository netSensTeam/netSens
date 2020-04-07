import logging
import os
from importlib import import_module
import mlog
logger = logging.getLogger('proc')

def getPackages(dir):
    for pname in os.listdir(dir):
        if pname in ['__init__.py', '__init__.pyc']:
            continue
        parts = pname.split('.')
        if len(parts) == 1:
            continue
        if parts[-1] != 'py':
            continue
        yield '.'.join(parts[:-1])

def load(mqc, dbc, lock, env):
    for pname in getPackages('networker/processors'):
        try:
            logger.info('loading processor %s', pname)
            module = import_module('processors.%s' % pname)
            Processor(mqc, dbc, lock, module, env)
        except Exception as e:
            logger.error('Failed to load processor: %s', str(e))

class Processor:
    def __init__(self, mqc, dbc, lock, module, env):
        self.logger = logger
        self.topic = module.topic
        self.proc_func = module.process
        mlog.configLoggers([module.name], env.logs_folder, env.debug_mode)
        module.init(mqc, dbc, lock, logging.getLogger(module.name))
        mqc.on_topic(module.topic, self.process)

    def process(self, data):
        self.logger.info('new data on topic %s', self.topic)
        self.proc_func(data)