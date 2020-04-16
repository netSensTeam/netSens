from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/networks/<uuid>/rename', ['POST'])
class RenameNetworkEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):  
        uuid = path_data['uuid']
        name = request_data.json['name']
        self.logger.debug(f'Rename request for network {uuid}')
        self.logger.debug(f'Renaming network {uuid} to {name}')
        self.publish('renameNetwork', {'uuid': uuid, 'name': name})
        return dumps({'success': True}), 200