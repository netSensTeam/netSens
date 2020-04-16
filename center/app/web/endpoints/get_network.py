from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/networks/<uuid>', ['GET'])
class GetNetworkEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):        
        uuid = path_data['uuid']
        network = self.dbClient.db.networks.find_one({'uuid': uuid})
        plugins = self.dbClient.db.plugins.find({})
        if not network:
            self.logger.warning('request for unknown network %s', uuid)
            return dumps({
                'success': False,
                'error': 'Unknown network with this uuid'
            }), 404
        else:
            return dumps({
                'success': True,
                'plugins': plugins,
                'network': network
            }), 200