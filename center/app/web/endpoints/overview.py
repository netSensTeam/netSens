from bson.json_util import dumps
from endpoints import _endpoint

@_endpoint.register('/api/overview', ['GET'])
class GetOverviewEndpoint(_endpoint.Endpoint):
    def handle(self, path_data, request_data):        
        networks = self.dbClient.getNetworksOverview()
        monitor = self.dbClient.db.monitor.find()
        jobs = self.dbClient.db.jobs.find({'finished':False})
        return dumps({
            'success': True,
            'networks': networks,
            'monitor': monitor,
            'jobs': jobs
        }), 200