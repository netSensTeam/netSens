from processors import _processor as processor

@processor.register('deviceAddRoles')
class DeviceAddRolesProcessor(processor.Processor):
    def process(self, data):
        net_uuid = data['networkUUID']
        dev_uuid = data['deviceUUID']
        roles = data['roles']
        with self.networkLock(net_uuid) as net:
            if net:
                net.addDeviceRoles(dev_uuid, roles)