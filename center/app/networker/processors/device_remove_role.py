from processors import _processor as processor

@processor.register('deviceRemoveRole')
class DeviceRemoveRoleProcessor(processor.Processor):
    def processor(self, data):
        with self.networkLock(net_uuid) as net:
            if net:
                net.removeDeviceRole(dev_uuid, role)