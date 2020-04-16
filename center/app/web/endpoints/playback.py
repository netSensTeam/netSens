from bson.json_util import dumps
import uuid
import os
from endpoints import _endpoint

@_endpoint.register('/api/playback/<target_uuid>/<save_packet>', ['POST'])
class PlaybackEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):
        if 'file' not in request_data.files:
            self.logger.error('No file in request')
            return dumps({'success': False, 'error': 'No file selected'}), 400
        file = request_data.files['file']
        if file.filename == '':
            self.logger.error('No file in request')
            return dumps({'success': False, 'error': 'No file selected'}), 400
        if path_data['save_packet'] == 'save':
            persist = True
        else:
            persist = False
            
        fileparts = file.filename.split('.')
        filename = '%s-%s.%s' % (fileparts[0], uuid.uuid4().hex, fileparts[1])
        self.logger.info('uploading file: %s', filename)
        file.save(os.path.join(self.env.pbak_folder, filename))
        self.mqClient.publish('playbackRequest', {'file':filename, 'targetNetworkId': path_data['target_uuid'], 'persist': persist})
        return dumps({'success': True}), 200