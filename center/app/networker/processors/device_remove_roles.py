from processors import _processor as processor

@processor.register('deviceRemoveRoles')
class DeviceRemoveRoleProcessor(processor.Processor):
    def process(self, data):
        net_uuid = data['networkUUID']
        dev_uuid = data['deviceUUID']
        roles = data['roles']
        with self.networkLock(net_uuid) as net:
            if net:
                device = net.findDevice(dev_uuid)
                if device:
                    device.removeRoles(roles)