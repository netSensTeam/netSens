from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/networks/<net_uuid>/devices/<dev_uuid>/plugins/<plg_uuid>', ['POST'])
class UsePluginEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):    
        net_uuid = path_data['net_uuid']
        dev_uuid = path_data['dev_uuid']
        plg_uuid = path_data['plg_uuid']
        topic = 'plugin-device-%s' % plg_uuid
        device = self.dbClient.getDevice(net_uuid, dev_uuid)
        if device:
            self.publish(topic, device)
        return dumps({'success':True}), 200