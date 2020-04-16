import logging
from importlib import import_module
import processors
from ns_utils import getPackages

logger = logging.getLogger('proc')

def loadProcessors(mqc, dbc, nlock, env):
    for pname in getPackages('processors'):
        try:
            logger.info(f'loading processor {pname}')
            import_module(f'processors.{pname}')
        except Exception as e:
            logger.error(f'failed to load processor {pname}: {e!r}')
    processors.load(mqc, dbc, nlock, env)