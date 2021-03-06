logger = None
name = 'FingerBank'
uuid = 'plugin-fb-123'
level = 'device'

def setLogger(lgr):
    global logger
    logger = lgr

import json
import requests

key = '1a59215c58c85c7555523e153e4b991134934587'
api = 'https://api.fingerbank.org/api/v2/combinations/interrogate?key=<key>'
api = api.replace('<key>', key)

def processDevice(device, manual=True):
    if not manual:
        return None
    if not 'extraData' in device:
        logger.info('device has no dhcp information')
        return None
    if not 'dhcpFingerPrint' in device['extraData']:
        logger.info('device has no dhcp information')
        return None

    try:
        dhcp_fp = device['extraData']['dhcpFingerPrint']
        encoded_data = json.dumps({'dhcp_fingerprint': str(dhcp_fp)[1:-1].replace(" ","")}).encode('utf-8')
        logger.debug('encoded_data: %s', encoded_data)
        headers = {
            "Content-type": "application/json"
        }
        response = requests.get(api, data=encoded_data)
        data = response.json()
        if 'errors' in data:
            logger.error('error in fingerbank reponse: %s', str(data['errors']))
            return None
        logger.debug('response: %s', data['device'])
        return {'OS': data['device']['name']}
    except Exception as e:
        logger.error('Error processing fingerbank request: %s' % str(e))
        return None