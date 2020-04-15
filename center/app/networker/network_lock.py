import threading
from entities import network
import contextlib

class NetworkLock:
    def __init__(self, mongo):
        self.mongo = mongo
        self.network_locks = {}
        self.llock = threading.Lock()
       
    @contextlib.contextmanager
    def __call__(self, uuid, saveBack=False):
        with self.llock:
            if not uuid in self.network_locks:
                self.network_locks[uuid] = threading.Lock()
        with self.network_locks[uuid]:
            net = self.mongo.db.networks.find_one({'uuid': uuid})
            if net:
                net = network.Network(net)
            yield net
            if net and saveBack:
                mongo.saveNetwork(net.serialize())   