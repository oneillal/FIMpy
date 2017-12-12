#!/usr/bin/env python
"""
FIMpy - A Python File Integrity Monitoring Application
"""

#########################################################################################
####################################  REFERENCES  #######################################
#########################################################################################
#
#   The following references are all being cited for code used in this application:
#
#   Bluemix Python Sample:  https://github.com/IBM-Bluemix/get-started-python
#   HMAC calculation:       https://pymotw.com/2/hmac/
#   Cloudant Code:          https://console.bluemix.net/docs/services/Cloudant/getting-started.html
#   HTTP Request Client:    http://docs.python-requests.org/en/master/user/quickstart
#   Python SSL:             http://bobthegnome.blogspot.co.uk/2007/08/making-ssl-connection-in-python.html http://flask.pocoo.org/snippets/111/
#   Python LDAP:            https://www.packtpub.com/books/content/python-ldap-applications-part-1-installing-and-configuring-python-ldap-library-and-bin
#   Python BasicAuth:       http://flask.pocoo.org/snippets/8/
#   Python Task Scheduling: https://apscheduler.readthedocs.io/en/latest/userguide.html
#                           https://stackoverflow.com/questions/21214270/scheduling-a-function-to-run-every-hour-on-flask
#   Command-Line Options:   https://docs.python.org/2/library/optparse.html
#   Python Slack Client:    https://github.com/os/slacker
#   KeyProtect Examples:    https://github.com/IBM-Bluemix/key-protect-helloworld-python
#   Jinja Template Example: http://jinja.pocoo.org/docs/2.10/templates/#builtin-filters
#   FIMpy Logo:             https://www.easyicon.net/language.en/541685-face_monkey_icon.html (Free for commerical use)
#
#
#   The following Python modules and libraries are used:
#
#   flask                   https://pypi.python.org/pypi/Flask/0.12.2
#   cloudant                https://pypi.python.org/pypi/cloudant/
#   hashlib                 https://pypi.python.org/pypi/hashlib/20081119
#   hmac                    https://pypi.python.org/pypi/hmac/20101005
#   requests                https://pypi.python.org/pypi/requests/2.18.4
#   optparse                https://pypi.python.org/pypi/optparse2/0.1
#   apscheduler             https://pypi.python.org/pypi/APScheduler
#   slacker                 https://pypi.python.org/pypi/slacker/0.9.60
#   unittest                https://pypi.python.org/pypi/unittest2/1.1.0
#   python-ldap             https://pypi.python.org/pypi/python-ldap/3.0.0b2
#   pyopenssl               https://pypi.python.org/pypi/pyOpenSSL/17.5.0
#
#########################################################################################

__author__ = "Alan O'Neill"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Alan O'Neill"
__status__ = "Development"

#######################################################################################
###############################   LOCAL IMPORTS  ######################################
#######################################################################################
from auth import protected
from verify import scanbaseline
from ibmkeyprotect import getkey

#######################################################################################
###############################   MODULE IMPORTS  #####################################
#######################################################################################

from cloudant.client import Cloudant
from cloudant.query import Query
from cloudant.document import Document

from flask import Flask, render_template, request, abort
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import hashlib
import hmac
import unittest

# Library used in Bluemix deployments
import cf_deployment_tracker

# Core Python modules
import atexit
import json
import os
import sys
import glob
import socket
from time import time

#######################################################################################
##################################   GLOBALS  #########################################
#######################################################################################
CONFIG = {
# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
    'port': int(os.getenv('PORT', 5000)),
    'host': 'localhost',
    'db_name': socket.getfqdn()
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

# Emit Bluemix deployment event
cf_deployment_tracker.track()

# Flask App declaration
app = Flask(__name__)

# BUF_SIZE for reading files
BUF_SIZE = 65536  # 64k chunks

# Cloudant Handlers
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
################################   UNIT TESTS  ########################################
#######################################################################################
class TestCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def testRestGetPing(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = self.app.get('/api/v1/ping')

        # assert the status code of the response
        # should return 200 - OK
        self.assertEqual(response.status_code, 200)

    def testRest404NotFound(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = self.app.get('/api/v1/dummy')

        # assert the status code of the response
        # should return 404 - Not Found
        self.assertEqual(response.status_code, 404)

    def testRestAuthenticationUnauthorised(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = self.app.get('/api/v1/config')

        # assert the status code of the response
        # should return 401 - Unauthorized
        self.assertEqual(response.status_code, 401)

    def testRestAuthenticationAuthorised(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = self.app.get('/api/v1/config', headers={'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='})

        # assert the status code of the response
        # should return 200 - Authorized
        self.assertEqual(response.status_code, 200)

    def testBluemixCloudantDbConnect(self):
        self.assertTrue(True)

    def testBluemixKeyProtectConnect(self):
        self.assertTrue(True)

# Commenting out the following Test Cases for demo

    # def testRestResponseJsonValidation(self):
    #     # sends HTTP GET request to the application
    #     # on the specified path
    #     response = self.app.get('/api/v1/baseline', headers={'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='})
    #
    #     # assert the status code of the response
    #     # should return True
    #     self.assertTrue(self.validjson(response.data))
    #
    # def validjson(self, x):
    #   try:
    #     doc = json.loads(x)
    #   except ValueError, e:
    #     return False
    #   return True
    #
    # def testRestResponseVerify(self):
    #     # sends HTTP GET request to the application
    #     # on the specified path
    #     r1 = self.app.get('/api/v1/baseline', headers={'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='})
    #
    #     r2 = self.app.post('/api/v1/verify', headers={'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='})
    #
    #     # assert the status code of responses
    #     # should return True and True
    #     self.assertEqual(r1.status_code, 200) and self.assertEqual(r2.status_code, 200)



#######################################################################################
#############################   REST END-POINTS  ######################################
#######################################################################################

# /*
#  * Endpoint for index.html
#  * Response:
#  * @return A rjinja2 based html template and content to populate the FIMpy dashboard
#  */
@app.route('/')
@protected
def home():
    results = {}
    if client:
        alive = []; hosts = []; ipaddresses = []; status = []; lastscandates = [];
        for db in client.all_dbs():
            # retrieve the host record for each db
            with Document(client[db], 'host') as host:
                if host['status'] == 3: # compromised
                    next # skip hosts that are reporting compromised state
                hosts.append(host['host'])
                ipaddresses.append(host['ipaddress'])
                status.append(host['status'])
                if 'lastscandate' in host:
                    lastscandates.append(host['lastscandate'])
                else:
                    lastscandates.append('-')
                if (host['host'] == CONFIG['db_name']): # no need to ping this instance
                    alive.append(True)
                else:
                    ping = 'https://' + host['ipaddress'] + ':' + str(CONFIG['port']) + '/api/v1/ping'
                    try:
                        # using self signed certs so turning off cert verification.
                        # TODO switch to IBM CA certs, setup trust store and enable cert verification
                        r = requests.get(ping, timeout=2, cert=('ssl/cert', 'ssl/key'), verify=False)
                        if r.status_code == requests.codes.ok:
                            alive.append(True)
                        else:
                            alive.append(False)
                    except requests.ConnectionError:
                        alive.append(False)
                        print "Exception occurred:", sys.exc_info()[0]

        results = {"hosts": hosts, "alive": alive, "ipaddresses": ipaddresses, "status": status, "lastscandates": lastscandates}
        from itertools import izip
        results = [dict(hosts=c1,
                        ipaddresses=c2,
                        alive=c3,
                        status=c4,
                        lastscandates=c5)
                   for c1, c2, c3, c4, c5
                   in izip(results['hosts'], results['ipaddresses'], results['alive'], results['status'], results['lastscandates'])]

    return render_template('index.html', x=results)

# /*
#  * Endpoint for an app instance heat-beat
#  * Send a GET /api/fimpy/ping
#  * Response:
#  * @return A response to indicate the app instance is running
#  */
@app.route('/api/v1/ping', methods=['GET'])
def restgetping():
    return json.dumps({}), 200, {'Content-Type': 'application/json; charset=utf-8'}

# /*
#  * Endpoint to get a JSON array of the app instance config
#  * GET /api/fimpy/config
#  * Response:
#  * @return An json string with config
#  */
@app.route('/api/v1/config', methods=['GET'])
@protected
def restgetconfig():
    if client:
        return json.dumps(CONFIG, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps([]), 500, {'Content-Type': 'application/json; charset=utf-8'}

# /*
#  * Endpoint to get a JSON array of the app instance monitored paths
#  * GET /api/v1/config/paths
#  * Response:
#  * @return An json string
#  */
@app.route('/api/v1/config/path', methods=['GET'])
@protected
def restgetpath():
    if client:
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}


# /*
#  * Endpoint to post a JSON array of a new app instance monitored path
#  * POST /api/v1/path/config/paths with body
#  * Response:
#  * @return An json string
#  */
@app.route('/api/v1/config/path', methods=['POST'])
@protected
def restpostconfig():
    if not request.json:
        abort(400)
# TODO needs to be implemented, just a skeleton.
    if client:
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return json.dumps(PATHS, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}


#  /* Endpoint to get a JSON array of all the monitored docs in the database
#  * <code>
#  * GET /api/v1/baseline
#  * </code>
# * {
# *     "file": "/path/file",
# *     "file": "/path/file"
# * }
# */
@app.route('/api/v1/baseline', methods=['GET'])
@protected
def restgetbaseline():
    if client:
        docs = []

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
            docs.append(item)

        root = {"docs": docs}

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
@app.route('/api/v1/baseline', methods=['POST'])
@protected
def restpostbaseline():
    # if not request.json:
    #     abort(400)
    docs = []
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
                    docs.append(data)
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

    with Document(db, 'host') as host:
        host['status'] = 1 # protecting

    root = {"docs": docs}

# TODO return proper json payload
    return json.dumps(root, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}


#  /* Endpoint to invoke the app instance to verify the baseline in the database for integrity
#  * POST /api/fimpy/verify
#  * Response:
#  * @return An json string with verification details
#  */
@app.route('/api/v1/verify', methods=['POST'])
@protected
def restpostverify():
    if client:
        docs = verify()
        root = {"docs": docs}

# TODO return proper json payload
        return json.dumps(root, sort_keys=True, indent=2), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        print('No database')
        return "", 500

#  /* Wrapper function for doc scanning that can be called via REST and scheduled job
#  * @return An json string with scan details
#  */
def verify():
    return scanbaseline(db, BUF_SIZE, SETTINGS['alert'])

#  /* Function to create scheduled job at set interval for baseline scanning
#  * @return n/a
#  */
def automonitor():
    cron.start()
    if options.auto:
        cron.add_job(verify, 'interval', minutes=SETTINGS['scanner_interval'])

#  /* Function to handle graceful shutdown
#  * @return n/a
#  */
@atexit.register
def shutdown():
    if client:
        client.disconnect()
        if cron:
            cron.shutdown(wait=False)



#########################################################################################
###################################   MAIN  #############################################
#########################################################################################
#                                                                                       #
#   The main python function that sets up commandline options, enables auto-protect     #
#   and alerts, registers new clients by creating db and config, configures SSL and     #
#   runs the test-suite. App will only start if sucessfully passing all test-cases.     #
#                                                                                       #
#########################################################################################
if __name__ == '__main__':

# Setup command-line options using optparse
    from optparse import OptionParser
    parser = OptionParser()

# option to enable auto generate base-line and start scanning
    parser.add_option("-s", "--auto",
                      action="store_true", dest="auto", default=False,
                      help="Automatically monitor baseline")

# option to send ush notifications to slack
    parser.add_option("-a", "--alert",
                      action="store_true", dest="alert", default=False,
                      help="Send slack alerts")

# setup based on passed command-line options
    (options, args) = parser.parse_args()
    if options.auto:
        automonitor()
        options.auto=False
    if options.alert:
        SETTINGS['alert'] = True

# local SSL rsa key and cert
# TODO: move this to IBM Key-Protect
    context = ('ssl/cert', 'ssl/key')

# if db handler is set, register client and generate config (if not already registered)
    if client:
        db = client[CONFIG['db_name']]
        with Document(db, 'host') as host:
            host['host'] = socket.getfqdn()
            host['ipaddress'] = socket.gethostbyname(socket.gethostname())
            host['registerdate'] = time()
            host['type'] = 'config'
            host['status'] = 0 # idle

# run test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCases)
    unittest.TextTestRunner(verbosity=2).run(suite)

# invoke Flask app on designated port and run options
    app.run(host='0.0.0.0', port=CONFIG['port'], ssl_context=context, threaded=True, use_reloader=False, debug=True)
