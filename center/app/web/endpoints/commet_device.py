from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/networks/<net_uuid>/devices/<dev_uuid>/comment', ['POST'])
class CommentDeviceEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):    
        net_uuid = path_data['net_uuid']
        dev_uuid = path_data['dev_uuid']
        self.publish(
            'deviceExtraData',
            {
                'networkUUID': net_uuid,
                'deviceUUID': dev_uuid,
                'extraData': {'comment': request_data.json['comment']}
            }
        )
        return dumps({'success':True}), 200