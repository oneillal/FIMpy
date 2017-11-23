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
from func import scanfiles

from cloudant.client import Cloudant
from cloudant.query import Query

from flask import Flask, render_template, request, abort

from apscheduler.schedulers.background import BackgroundScheduler

import atexit
import cf_deployment_tracker
import json
import os
import glob
import socket
import hashlib
import hmac

#######################################################################
CONFIG = {
# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
    'port': int(os.getenv('PORT', 5000)),
    'host': 'localhost',
    'db_name': socket.getfqdn(),
    'user': 'user',
    'password': 'password',
    'slack_token': os.getenv('SLACKTOKEN', 'xoxp-9999999999')
}

SETTINGS = {
    'scanner_interval': 1
}

PATHS = {
# Array of paths to be monitored e.g. 'paths': ['/path1', '/path2/path3']
#   'paths': ['/bin', '/usr/bin/python2.7']
    'paths': ['test', 'static']
}
#######################################################################

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

client = None
db = None

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
#       client.delete_database(CONFIG['db_name'])  # delete existing db for dev
        print CONFIG['db_name']
        db = client.create_database(CONFIG['db_name'], throw_on_exists=False)


#######################################################################################
#######################################################################################
#######################################################################################

@app.route('/')
@protected
def home():
    return render_template('index.html')

# /*
#  * Endpoint to get a JSON array of all the monitored files in the database
#  * Send a POST request to localhost:8000/api/fimpy with body
#  * Response:
#  * @return An message string
#  */
@app.route('/api/fimpy/test', methods=['GET'])
@protected
def test():
    print ""
    return json.dumps({}), 200, {'Content-Type': 'application/json; charset=utf-8'}

# /*
#  * Endpoint to get a JSON array of all the monitored files in the database
#  * Send a POST request to localhost:8000/api/fimpy with body
#  * Response:
#  * @return An message string
#  */
@app.route('/api/fimpy/config', methods=['GET'])
@protected
def getconfig():
    if client:
        return json.dumps(CONFIG, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps([]), 500, {'Content-Type': 'application/json; charset=utf-8'}

# /*
#  * Endpoint to get a JSON array of all the monitored files in the database
#  * Send a POST request to localhost:8000/api/fimpy with body
#  * Response:
#  * @return An message string
#  */
@app.route('/api/fimpy/config/path', methods=['GET'])
@protected
def getpath():
    if client:
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}


# /*
#  * Endpoint to get a JSON array of all the monitored files in the database
#  * Send a POST request to localhost:8000/api/fimpy with body
#  * Response:
#  * @return An message string
#  */
@app.route('/api/fimpy/config/path', methods=['POST'])
@protected
def setpath():
    if not request.json:
        abort(400)
    if client:
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}

# /* Endpoint to get the monitored files from the database.
#  * Endpoint to get a JSON array of all the monitored files in the database
#  * <code>
#  * GET http://localhost:8000/api/fimpy
#  * </code>
# * {
# *     "file": "/path/file",
# *     "file": "/path/file"
# * }
# */
@app.route('/api/fimpy', methods=['GET'])
@protected
def getfileinfo():
    if client:
        items = []

        # retrieve docs of type proof
        query = Query(db, selector={'type': {'$eq': 'proof'}})

        for document in query.result:
            item = {"file": document['file']}
            item["host"] = document['host']
            item["ipaddress"] = document['ipaddress']
            item["size"] = document['size']
            item["createdate"] = document['createdate']
            item["modifydate"] = document['modifydate']
            item["hash"] = document['hash']
            item["hmac"] = document['hmac']
            items.append(item)

            print(document['file'])
            print('hash db> ' + document['hash'])
            print('hmac db> ' + document['hmac'])

        array = {"file": items}
        root = {"files": array}

        return json.dumps(root, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps([]), 500, {'Content-Type': 'application/json; charset=utf-8'}

# /*
#  * Endpoint to get a JSON array of all the monitored files in the database
#  * Send a POST request to localhost:8000/api/fimpy with body
#  * Response:
#  * @return An message string
#  */
@app.route('/api/fimpy', methods=['POST'])
@protected
def writefiledata():
    if not request.json:
        abort(400)
    items = []
    for path in PATHS['paths']:
#TODO add path based monitoring rules
        for file in glob.glob(os.path.join(path, '*')):
            if os.path.isfile(file):
                f = open(file, 'rb')
#TODO add exception handling
                try:
                    sha256 = hashlib.sha256()
                    digest = hmac.new('secret-shared-key-goes-here', '', hashlib.sha256)
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
                            'type': 'proof'}
                    db.create_document(data)
                    items.append(data)

    array = {"file": items}
    root = {"files": array}

# TODO return proper json payload
    print 'Records added to db'
    return json.dumps(root, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}

# /* Endpoint to get the monitored files from the database.
#  * Endpoint to get a JSON array of all the monitored files in the database
#  * <code>
#  * GET http://localhost:8000/api/fimpy
#  * </code>
# * {
# *     "file": "/path/file",
# *     "file": "/path/file"
# * }
# */

@app.route('/api/fimpy/scan', methods=['POST'])
@protected
def scan():
    if client:
        scanner()

# TODO return proper json payload
        return "", 200
    else:
        print('No database')
        return "", 500

def scanner():
    scanfiles(db, BUF_SIZE)


@atexit.register
def shutdown():
    if client:
        client.disconnect()
        cron.shutdown(wait=False)

if __name__ == '__main__':
    context = ('cert', 'key')
    # Kick-off background thread to scan files
    cron = BackgroundScheduler(daemon=True)
    cron.start()
    cron.add_job(scanner, 'interval', minutes=SETTINGS['scanner_interval'])
    app.run(host='0.0.0.0', port=CONFIG['port'], ssl_context=context, threaded=True, use_reloader=False, debug=True)