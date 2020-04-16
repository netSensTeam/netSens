from processors import _processor as processor

@processor.register('clearNetwork')
class ClearNetworkProcessor(processor.Processor):
    def process(self, data):
        uuid = data['uuid']
        with self.networkLock(uuid) as net:
            if net:
                net.clear()