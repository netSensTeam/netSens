from importlib import import_module
import logging
from ns_utils import getPackages
import endpoints

logger = logging.getLogger('endpoint')

def loadEndpoints(webApp, dbClient, mqClient, env):
    for ename in getPackages('endpoints'):
        try:
            logger.info(f'Loading endpoint {ename}')
            import_module(f'endpoints.{ename}')
        except Exception as e:
            logger.error(f'Failed to import module: {e}')
    endpoints.load(webApp, dbClient, mqClient, env)
        