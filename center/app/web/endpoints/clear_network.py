from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/networks/<uuid>/clear', ['POST'])
class ClearNetworkEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):    
        uuid = path_data['uuid']
        self.publish('clearNetwork', {'uuid': uuid,})
        return dumps({'success': True}), 200
