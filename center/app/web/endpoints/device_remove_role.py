from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/networks/<net_uuid>/devices/<dev_uuid>/roles/<role>', ['DELETE'])
class DeviceRemoveRoleEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):    
        net_uuid = path_data['net_uuid']
        dev_uuid = path_data['dev_uuid']
        dev_role = path_data['role']
        self.publish(
            'deviceRemoveRole',
            {
                'networkUUID': net_uuid,
                'deviceUUID': dev_uuid,
                'role': dev_role
            }
        )
        return dumps({'success':True}), 200