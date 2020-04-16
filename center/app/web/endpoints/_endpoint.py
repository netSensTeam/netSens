from abc import ABC, abstractmethod
from flask import request
import logging
import mlog

logger = logging.getLogger('endpoint')

class Endpoint(ABC):
    def __init__(self, dbClient, mqClient, logger, env):
        self.dbClient = dbClient
        self.mqClient = mqClient
        self.logger = logger
        self.env = env
        super().__init__()
            
    def publish(self, topic, data):
        self.mqClient.publish(topic, data)
        
    @abstractmethod
    def handle(path_data, request_data):
        pass
        
registered_endpoints = []

def register(url, methods):
    def decorator(cls):
        logger.debug(f'Registering class {cls.__name__} with url {url} and methods {methods}')
        cls.url = url
        cls.methods = methods
        
        registered_endpoints.append(cls)
    return decorator

def _make(ep, dbClient, mqClient, env):
    def _(*args, **kwargs):
        inst = ep(dbClient, mqClient, logging.getLogger(ep.__name__), env)
        logger.debug(f'Endpoint instance is of type {type(inst)}')
        path_data = kwargs
        logger.debug(f'invoked endpoint {ep.__name__}')
        logger.debug(f'path data: {path_data}')
        logger.debug(f'request data: {request}')
        return inst.handle(path_data, request)
    return _
    
def load(flaskApp, dbClient, mqClient, env):
    for ep in registered_endpoints:
        mlog.configLoggers([ep.__name__], env.logs_folder, env.debug_mode)    
        logger.debug(f'Adding flask url rule {ep.url} with {ep.__name__}')
        flaskApp.add_url_rule(ep.url, ep.__name__, _make(ep, dbClient, mqClient, env), methods=ep.methods)