from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/networks/<uuid>', ['DELETE'])
class RemoveNetworkEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):    
        uuid = path_data['uuid']
        self.publish('removeNetwork', {'uuid': uuid,})
        return dumps({'success': True}), 200
