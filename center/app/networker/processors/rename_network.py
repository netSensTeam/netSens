from processors import _processor as processor

@processor.register('renameNetwork')
class DeviceRemoveRoleProcessor(processor.Processor):
    def process(self, data):
        uuid = data['uuid']
        name = data['name']
        with self.networkLock(uuid) as net:
            if net:
                self.logger.debug(f'Renaming network {net.name} to {name}')
                net.name = name
            else:
                self.logger.error(f'Cannot rename network {uuid}: not found')