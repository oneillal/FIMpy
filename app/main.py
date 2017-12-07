#!/usr/bin/env python
"""
FIMpy - A Python File Integrity Monitoring Application

"""

__author__ = "Alan O'Neill"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Alan O'Neill"
__status__ = "Development"

# local imports
from auth import protected
from func import scandocs

from cloudant.client import Cloudant
from cloudant.query import Query
from cloudant.document import Document

from flask import Flask, render_template, request, abort

from apscheduler.schedulers.background import BackgroundScheduler

import atexit
import cf_deployment_tracker
import json
import os
import sys
import glob
import socket
import hashlib
import hmac
import requests
from ibmkeyprotect import getkey

#######################################################################
CONFIG = {
# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
    'port': int(os.getenv('PORT', 5000)),
    'host': 'localhost',
    'db_name': socket.getfqdn(),
    'user': 'user',
    'password': 'password'
}

SETTINGS = {
    'scanner_interval': 1,
    'alert': False
}

PATHS = {
# Array of paths to be monitored e.g. 'paths': ['/path1', '/path2/path3']
#   'paths': ['/bin', '/usr/bin/python2.7']
    'paths': ['test']
}
#######################################################################

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

# BUF_SIZE for reading files
BUF_SIZE = 65536  # 64k chunks

client = None
db = None

# Define a background scheduler to scan docs
cron = BackgroundScheduler(daemon=True)

# Initialise Bluemix and Cloudant configuration
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
#       client.delete_database(CONFIG['db_name'])  # delete existing db for dev
        db = client.create_database(CONFIG['db_name'], throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(CONFIG['db_name'], throw_on_exists=False)

#######################################################################################
#######################################################################################
#######################################################################################

@app.route('/')
@protected
def home():
    results = {}
    if client:
        alive = []; hosts = []; ipaddresses = []; status = [];
        for db in client.all_dbs():
            # retrieve the bot record for each db
            with Document(client[db], 'bot') as bot:
                if bot['status'] == 1: # compromised
                    next # skip hosts that are reporting compromised state
                hosts.append(bot['host'])
                ipaddresses.append(bot['ipaddress'])
                status.append(bot['status'])
                if (bot['host'] == CONFIG['db_name']): # no need to ping this instance
                    alive.append(True)
                else:
                    ping = 'https://' + bot['ipaddress'] + ':5000/api/fimpy/ping'
                    try:
                        r = requests.get(ping, timeout=2, cert=('ssl/cert', 'ssl/key'), verify=False)
                        if r.status_code == requests.codes.ok:
                            alive.append(True)
                        else:
                            alive.append(False)
                    except requests.ConnectionError:
                        alive.append(False)
                        print "Exception occurred:", sys.exc_info()[0]

        results = {"hosts": hosts, "alive": alive, "ipaddresses": ipaddresses, "status": status}
        from itertools import izip
        results = [dict(hosts=c1, ipaddresses=c2, alive=c3, status=c4) for c1, c2, c3, c4 in izip(results['hosts'], results['ipaddresses'], results['alive'], results['status'])]
    return render_template('index.html', x=results)

# /*
#  * Endpoint for an app instance heat-beat
#  * Send a GET request to localhost:8000/api/fimpy/ping
#  * Response:
#  * @return A response to indicate the app instance is running
#  */
@app.route('/api/v1/ping', methods=['GET'])
def ping():
    return json.dumps({}), 200, {'Content-Type': 'application/json; charset=utf-8'}

# /*
#  * Endpoint to get a JSON array of the app instance config
#  * Send a GET request to localhost:5000/api/fimpy/config
#  * Response:
#  * @return An json string with config
#  */
@app.route('/api/v1/config', methods=['GET'])
@protected
def getconfig():
    if client:
        return json.dumps(CONFIG, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps([]), 500, {'Content-Type': 'application/json; charset=utf-8'}

# /*
#  * Endpoint to get a JSON array of the app instance monitored paths
#  * Send a GET request to localhost:5000/api/fimpy/config/paths
#  * Response:
#  * @return An json string
#  */
@app.route('/api/v1/config/path', methods=['GET'])
@protected
def getpath():
    if client:
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}


# /*
#  * Endpoint to post a JSON array of a new app instance monitored path
#  * Send a POST request to localhost:5000/api/fimpy/path/config/paths with body
#  * Response:
#  * @return An json string
#  */
@app.route('/api/v1/config/path', methods=['POST'])
@protected
def setpath():
    if not request.json:
        abort(400)
    if client:
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}


#  /* Endpoint to get a JSON array of all the monitored docs in the database
#  * <code>
#  * GET http://localhost:5000/api/fimpy
#  * </code>
# * {
# *     "file": "/path/file",
# *     "file": "/path/file"
# * }
# */
@app.route('/api/v1/docs', methods=['GET'])
@protected
def getfileinfo():
    if client:
        items = []

        # retrieve docs of type data
        query = Query(db, selector={'type': {'$eq': 'doc'}})

        for document in query.result:
            item = {"file": document['_id']}
            item["host"] = document['host']
            item["ipaddress"] = document['ipaddress']
            item["size"] = document['size']
            item["createdate"] = document['createdate']
            item["modifydate"] = document['modifydate']
            item["hash"] = document['hash']
            item["hmac"] = document['hmac']
            item["status"] = document['status']
            items.append(item)

        root = {"docs": items}

        return json.dumps(root, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps([]), 500, {'Content-Type': 'application/json; charset=utf-8'}

# /*
#  * Endpoint to invoke the app to scan the monitored paths and store file data in the database
#  * Send a POST request to localhost:8000/api/fimpy
#  * Response:
#  * @return An json string with file data added to the database
#  */
@app.route('/api/v1/docs', methods=['POST'])
@protected
def writefiledata():
    # if not request.json:
    #     abort(400)
    items = []
    for path in PATHS['paths']:
#TODO add path based monitoring rules
        for file in glob.glob(os.path.join(path, '*')):
            if os.path.isfile(file):
                f = open(file, 'rb')
#TODO add exception handling
                try:
                    sha256 = hashlib.sha256()
                    digest = hmac.new(getkey(), '', hashlib.sha256)
                    while True:
                        block = f.read(BUF_SIZE)
                        if not block:
                            break
                        digest.update(block) # update the hmac for the next file block
                        sha256.update(block) # update the hash for the next file block
                finally:
                    f.close()

                # print("File: {0}".format(os.path.realpath(file)))
                # print("SHA256: {0}".format(sha256.hexdigest()))
                # print("HMAC: {0}".format(digest.hexdigest()))

                if client: # if db connection, then write to the db
                    data = {'host': socket.getfqdn(),
                            'ipaddress': socket.gethostbyname(socket.gethostname()),
                            'file': os.path.realpath(file),
                            'size': os.path.getsize(file),
                            'createdate': os.path.getctime(file),
                            'modifydate': os.path.getmtime(file),
                            'hash': sha256.hexdigest(),
                            'hmac': digest.hexdigest(),
                            'type': 'doc',
                            'status': 1}
                    # db.create_document(data)
                    items.append(data)
                    with Document(db, data['file']) as file:
                        file['host'] = data['host']
                        file['ipaddress'] = data['ipaddress']
                        file['size'] = data['size']
                        file['createdate'] = data['createdate']
                        file['modifydate'] = data['modifydate']
                        file['hash'] = data['hash']
                        file['hmac'] = data['hmac']
                        file['type'] = data['type']
                        file['status'] = data['status']

    with Document(db, 'bot') as bot:
        bot['status'] = 1 # protecting

    root = {"docs": items}

# TODO return proper json payload
    return json.dumps(root, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}


#  /* Endpoint to invoke the app instance to scan the monitored docs in the database for integrity
#  * POST http://localhost:5000/api/fimpy/scan
#  * Response:
#  * @return An json string with scan details
#  */
@app.route('/api/v1/scan', methods=['POST'])
@protected
def scan():
    if client:
        items = scanner()
        root = {"docs": items}

# TODO return proper json payload
        return json.dumps(root, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return "", 500


def scanner():
    return scandocs(db, BUF_SIZE, SETTINGS['alert'])

def autoprotect():
    if options.protect:
        cron.add_job(scanner, 'interval', minutes=SETTINGS['scanner_interval'])


@atexit.register
def shutdown():
    if client:
        client.disconnect()
        if cron:
            cron.shutdown(wait=False)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--scan",
                      action="store_true", dest="scan", default=False,
                      help="Automatically scan docs")
    parser.add_option("-a", "--alert",
                      action="store_true", dest="alert", default=False,
                      help="Send slack alerts")
    (options, args) = parser.parse_args()
    cron.start()
    if options.scan:
        autoprotect()
        options.protect=False
    if options.alert:
        SETTINGS['alert'] = True

    context = ('ssl/cert', 'ssl/key')

    if client:
        db = client[CONFIG['db_name']]
        with Document(db, 'bot') as bot:
            bot['host'] = socket.getfqdn()
            bot['ipaddress'] = socket.gethostbyname(socket.gethostname())
            bot['registerdate'] = ''
            bot['lastscandate'] = ''
            bot['type'] = 'config'
            bot['alive'] = True
            bot['status'] = 0 # idle

    app.run(host='0.0.0.0', port=CONFIG['port'], ssl_context=context, threaded=True, use_reloader=False, debug=True)