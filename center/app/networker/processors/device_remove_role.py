name = 'device_remove_role'
topic = 'deviceRemoveRole'

NetworkLock = None
logger = None
db_client = None
mq_client = None

def init(mq, db, nlock, lgr):
    global NetworkLock, logger, db_client, mq_client
    mq_client = mq
    db_client = db
    NetworkLock = nlock
    logger = lgr

def process(data):
    global db_client, NetworkLock
    net_uuid = data['networkUUID']
    dev_uuid = data['deviceUUID']
    role = data['role']
    with NetworkLock(net_uuid) as net:
        if net:
            net.removeDeviceRole(dev_uuid, role)