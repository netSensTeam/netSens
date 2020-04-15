import os
import subprocess
import sys
import shutil
import json
import platform

sysname = platform.system().lower()

env_file = 'public'
services_to_run = None
separate_window = True if sysname == 'windows' else False
i = 0 
while i < len(sys.argv):
    if sys.argv[i] == 'help':
        print('use to start required services for netSens')
        print('usage: python init.py [-e env_file_name] [-s service1,service2,...] [-nw]')
        print('-e env_file_name - sets the desired env file for the web service')
        print('-s service1,service2,... - loads only specified services from the service.json file. If not specified all services are loaded by default')
        print('-nw - supported only in windows. If used, all services will be run within the same shell window.')
        sys.exit(0)
    elif sys.argv[i] == '-e':
        env_file = sys.argv[i+1]
        i += 1
    elif sys.argv[i] == '-s':
        services_to_run = sys.argv[i+1].split(',')
        i += 1
    elif sys.argv[i] == '-nw':
        if sysname == 'windows':
            separate_window = False
    i += 1

service_file = f'services.{sysname}.json' 
with open(service_file, 'r') as fp:
    services = json.load(fp)

os.chdir('..')
env_path = f'app/web/env_{env_file}.py'
if not os.path.exists(env_path):
    raise Exception(f'ENV file {env_file} not found')
    sys.exit(0)
    
shutil.copyfile(env_path, 'app/web/env.py')

root_dir = os.getcwd()
dirlist = [
	'data',
	'data/mongo',
	'data/playback',
	'data/runtime',
	'data/runtime/playback',
	'data/runtime/monitor',
	'data/runtime/web',
	'data/runtime/networker',
	'data/logs',
	'data/logs/playback',
	'data/logs/monitor',
	'data/logs/web',
	'data/logs/networker',
	'data/logs/thirdparty'
]

for d in dirlist:
    dir = os.path.join(root_dir, d)
    if not os.path.exists(dir):
        print(f'creating dir: {dir}')
        os.mkdir(dir)

for service in services:
    if services_to_run and service['name'] not in services_to_run:
        continue
    if 'active' in service and not service['active']:
        continue
    print('starting service: %s' % service['name'])
    os.chdir(service['execPath'])
    cmd = service['cmd'].replace('%rd%', root_dir).split(' ')
    if separate_window:
        cmd.insert(0,'start')
    subprocess.Popen(cmd, shell=True)
    os.chdir(root_dir)