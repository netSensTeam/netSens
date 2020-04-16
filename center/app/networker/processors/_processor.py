from abc import ABC, abstractmethod
import logging
import mlog
processors = []
logger = logging.getLogger('proc')

class Processor(ABC):
    def __init__(self, mqClient, dbClient, networkLock, logger):
        self.mqClient = mqClient
        self.dbClient = dbClient
        self.networkLock = networkLock
        self.logger = logger
        super().__init__()
    
    @abstractmethod
    def process(self, data):
        pass
        

def register(topic):
    def register_decorator(cls):
        cls.topic = topic
        processors.append(cls)
        return cls
    return register_decorator
    
def _make(proc, mqClient, dbClient, nLock):
    def _(data):
        logger.info(f'Received data on topic: {proc.topic}')
        try:
            inst = proc(mqClient, dbClient, nLock, logging.getLogger(proc.__name__))
            logger.debug(f'Instantiated processor {proc.__name__}')
            inst.process(data)
        except Exception as e:
            logger.error(f'Failed to process data: {e}')
    return _
    
def load(mqClient, dbClient, nLock, env):
    for proc in processors:
        logger.info(f'Subscribing processor {proc.__name__} to topic {proc.topic}')
        mlog.configLoggers([proc.__name__], env.logs_folder, env.debug_mode)
        mqClient.on_topic(proc.topic, _make(proc, mqClient, dbClient, nLock))