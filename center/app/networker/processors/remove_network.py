from processors import _processor as processor

@processor.register('removeNetwork')
class DeviceRemoveRoleProcessor(processor.Processor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def process(self, data):
        uuid = data['uuid']
        with self.networkLock(uuid):
            self.dbClient.deleteNetwork(uuid)