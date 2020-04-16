from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/networks/<net_uuid>/devices/<dev_uuid>/analyze', ['GET'])
class AnalyzeDeviceEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):
        net_uuid = path_data['net_uuid']
        dev_uuid = path_data['dev_uuid']
        packets = self.dbClient.getDevicePackets(net_uuid, dev_uuid)
        return dumps({'success':True, 'packets': packets})