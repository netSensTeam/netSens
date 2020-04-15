from abc import ABC, abstractmethod
import mlog
processors = []

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
    
def load(mqClient, dbClient, nLock, env):
    for proc in processors:
        mlog.configLoggers(proc.__name__, env.logs_folder, env.debug_mode)
        def _(data):
            inst = proc.__init__(mqClient, dbClient, nLock, logging.getLogger(proc.__name__))
            inst.process(data)
        mqClient.on_topic(proc.topic, _)
        