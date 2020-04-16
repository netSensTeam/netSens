import time
from entities.network import Network
from entities.packet import Packet
from processors import _processor as processor

@processor.register('packetsBuffer')
class PacketsBufferProcessor(processor.Processor):
    def process(self, packets_buffer):
        self.logger.info('Processing new packet buffer with %d packets' % packets_buffer['numPackets'])
        start_time = time.time()
        network_queue = []
        org_uuid = packets_buffer['origin']

        packet_convert_time = time.time()
        packets = [Packet(pkt) for pkt in packets_buffer['packets']]
        elapsed_time = time.time() - packet_convert_time
        self.logger.debug(f'Packet parsing time is {elapsed_time} seconds')

        if 'target' in packets_buffer and packets_buffer['target']:
            target_uuid = packets_buffer['target']
        else:
            target_uuid = self.getTargetNetwork(org_uuid)
        
        if 'persist' in packets_buffer:
            save = packets_buffer['persist']
        else:
            save = True
        if save:
            self.logger.info('Packets will be persisted to DB')
        else:
            self.logger.info('Packets will not be persisted to DB')
        
        with self.networkLock(target_uuid) as net:
            net_start_time = time.time()
            net.process(packets, save=save)
            elapsed_time = time.time() - net_start_time
            self.logger.debug(f'Processing time for new network was {elapsed_time} seconds')
            if net.reprocess:
                network_queue.append(net)
                net.reprocess = False
        altered_networks = self.processNetworkQueue(network_queue)
        elapsed_time = time.time() - start_time
        self.logger.debug(f'Total processing time was {elapsed_time} seconds. Number of altered networks was {len(altered_networks)}')

        self.publishAlteredNetworks(altered_networks)

    def findNetworkMatch(self, net):
        if not net.gateways:
            return None
        networks = self.dbClient.db.networks.find({}, {'uuid': 1, 'gateways': 1})
        for cand_net in networks:
            if cand_net['uuid'] == net.uuid:
                continue
            cand_gtw = cand_net['gateways']
            if not set(cand_gtw).isdisjoint(set(net.gateways)):
                return cand_net['uuid']
        return None

    def getNetworkForOrigin(self, org_uuid):
        pairs = self.dbClient.db.origins.find({})
        for pair in pairs:
            if pair['originUUID'] == org_uuid:
                return pair['networkUUID']
        return None

    def addOriginNetwork(self, net_uuid, org_uuid):
        self.dbClient.db.origins.insert_one({
            'originUUID': org_uuid, 
            'networkUUID': net_uuid
            })

    def updateOriginNetwork(self, old_net_uuid, new_net_uuid):
        self.dbClient.db.origins.update({
                'networkUUID': old_net_uuid
            }, {
                '$set': {'networkUUID': new_net_uuid}
            },
            upsert=False)

    def getTargetNetwork(self, org_uuid):
        target_uuid = self.getNetworkForOrigin(org_uuid)
        if not target_uuid:
            net = Network.create()
            self.logger.debug('No target network was found, creating new network {net.uuid}')
            target_uuid = net.uuid
            self.dbClient.addNetwork(net.serialize())
            self.addOriginNetwork(target_uuid, org_uuid)
        return target_uuid

    def publishAlteredNetworks(self, altered_networks):
        for uuid in altered_networks:
            network_data = self.dbClient.db.networks.find_one({'uuid': uuid})
            if network_data:
                for device in network_data['devices']:
                    self.mqClient.publish('device', device)

    def mergeNetworks(self, to, fr, altered_networks):
        to.mergeNetwork(fr)
        altered_networks.append(to.uuid)
        altered_networks.remove(fr.uuid)
        self.dbClient.deleteNetwork(fr.uuid)
        self.updateOriginNetwork(fr.uuid, to.uuid)

    def processNetworkQueue(self, network_queue):
        if not network_queue:
            return []
        altered_networks = [network_queue[0].uuid]
        while network_queue:
            nex = network_queue.pop(0)
            with self.networkLock(nex.uuid):
                merge_uuid = self.findNetworkMatch(nex)
                
                if not merge_uuid:
                    continue

                with self.networkLock(merge_uuid) as merge_net:
                    self.mergeNetworks(merge_net, nex, altered_networks)
                    if merge_net.reprocess:
                        network_queue.append(merge_net)
                        merge_net.reprocess = False
        return altered_networks