import logging
import os
from importlib import import_module
import mlog
import processors
logger = logging.getLogger('proc')

def getPackages(dir):
    for pname in os.listdir(dir):
        if pname[0] == '_':
            continue
        parts = pname.split('.')
        if len(parts) == 1:
            continue
        if parts[-1] != 'py':
            continue
        yield '.'.join(parts[:-1])

def loadProcessors(mqc, dbc, nlock, env):
    for pname in getPackages('networker/processors'):
        try:
            logger.info(f'loading processor {pname}')
            import_module(f'processors.{pname}')
        except Exception as e:
            logger.error(f'failed to load processor {pname}: {e!r}')
    processors.load(mqc, dbc, nlock, env)