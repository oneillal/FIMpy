#!/usr/bin/env python
"""
FIMpy - A Python File Integrity Monitoring Application

"""
__author__ = "Alan O'Neill"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Alan O'Neill"
__status__ = "Development"

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import json
import socket
import os
import glob

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
# Array of paths to be monitored e.g. 'paths': ['/path1', '/path2/path3']
#   'paths': ['/bin', '/usr/bin/python2.7']
    'paths': ['test']
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
        client.delete_database(CONFIG['db_name']) # delete existing db for dev
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
        client.delete_database(CONFIG['db_name']) # delete existing db for dev
        db = client.create_database(CONFIG['db_name'], throw_on_exists=False)

        # Get all of the documents from my_database
        for document in db:
            # Look for all documents which do not match _design/
            if not pattern.match(document['_id']):
                print (document['_id'])
                document.delete()

@app.route('/')
def home():
    return render_template('index.html')

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
def getFileInfo():
    if client:
        for document in db:
            print(document['file'])
            print('hash db> ' + document['hash'])
            print('hmac db> ' + document['hmac'])
        return jsonify(list(map(lambda doc: doc['file'], db)))
    else:
        print('No database')
        return jsonify([])

# /*
#  * Endpoint to get a JSON array of all the monitored files in the database
#  * Send a POST request to localhost:8000/api/fimpy with body
#  * Response:
#  * @return An message string
#  */
@app.route('/api/fimpy', methods=['POST'])
def writeFileData():
    for path in CONFIG['paths']:
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
                            'createdate': os.path.getmtime(file),
                            'hash': sha256.hexdigest(),
                            'hmac': digest.hexdigest()}
                    db.create_document(data)
    return 'Records added to db'

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
@app.route('/api/fimpy/scan', methods=['GET'])
def scanFiles():
    if client:
        for document in db:
            sha256 = hashlib.sha256()
            digest = hmac.new('secret-shared-key-goes-here', '', hashlib.sha256)
            file = document['file']
            if os.path.isfile(file):
                f = open(file, 'rb')
                # TODO add exception handling
                try:
                    while True:
                        block = f.read(BUF_SIZE)
                        if not block:
                            break
                        digest.update(block)  # update the hmac for the next file block
                        sha256.update(block)  # update the hash for the next file block
                finally:
                    f.close()
            print(document['file'])
            print('hash db> ' + document['hash'])
            print('hash fs> ' + sha256.hexdigest())
            print('hmac db> ' + document['hmac'])
            print('hmac fs> ' + digest.hexdigest())

            if digest.hexdigest() == document['hmac']:
                print "match"
            else:
                print "data does not match"

        return jsonify(list(map(lambda doc: doc['file'], db)))
    else:
        print('No database')
        return jsonify([])


@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CONFIG['port'], debug=True)
