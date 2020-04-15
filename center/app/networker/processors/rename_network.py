from processors import _processor as processor

@processor.register('renameNetwork')
class DeviceRemoveRoleProcessor(processor.Processor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def process(self, data):
        uuid = data['uuid']
        with self.networkLock(data['uuid']):
            if net:
                net.name = data['name']