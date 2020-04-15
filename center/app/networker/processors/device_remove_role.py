from processors import _processor as processor

@processor.register('deviceRemoveRole')
class DeviceRemoveRoleProcessor(processor.Processor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def processor(self, data):
        with self.networkLock(net_uuid) as net:
            if net:
                net.removeDeviceRole(dev_uuid, role)