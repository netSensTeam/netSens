from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/networks/<net_uuid>/devices/<dev_uuid>/roles', ['POST'])
class DeviceAddRolesEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):    
        net_uuid = path_data['net_uuid']
        dev_uuid = path_data['dev_uuid']
        dev_roles = request_data.json['roles']
        self.publish(
            'deviceAddRoles',
            {
                'networkUUID': net_uuid,
                'deviceUUID': dev_uuid,
                'roles': dev_roles
            }
        )
        return dumps({'success':True}), 200