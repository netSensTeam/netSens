from processors import _processor as processor

@processor.register('deviceExtraData')
class DeviceExtraDataProcessor(processor.Processor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def process(self, data):
        net_uuid = data['networkUUID']
        dev_uuid = data['deviceUUID']
        ext_data = data['extraData']
        with self.networkLock(net_uuid) as net:
            if net:
                net.addDeviceData(dev_uuid, ext_data)