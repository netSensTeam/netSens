import threading
import logging
from flask import Flask, send_from_directory
from flask_cors import CORS
import endpointManager
logger = logging.getLogger('api')   
class APIServer:
    def __init__(self, env, mqClient, dbClient):
        self.debug = env.debug_mode
        self.port = env.flask_port
        self.app = Flask('netSensWeb')
        CORS(self.app)
        self.create_static_endpoints(env.static_files_folder)
        endpointManager.loadEndpoints(self.app, dbClient, mqClient, env)

    def create_static_endpoints(self, folder):
        @self.app.route('/<path:path>')
        def send(path):
            return send_from_directory(folder, path)
        
        @self.app.route('/')
        def sendIndex():
            return send_from_directory(folder, 'index.html')
        
    def start(self):
        self.app.run(host='0.0.0.0', port=self.port, debug=self.debug)