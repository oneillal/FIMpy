#!/usr/bin/env python
"""
FIMpy - A Python File Integrity Monitoring Application
"""

#########################################################################################
###################################  FUNC  ##############################################
#########################################################################################
#                                                                                       #
#   Python module for functions to make more modular and maintainable                   #
#                                                                                       #
#########################################################################################

__author__ = "Alan O'Neill"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Alan O'Neill"
__status__ = "Development"

import hashlib
import hmac
from os import path

from cloudant.query import Query
from cloudant.document import Document
from alert import alert_slack
from ibmkeyprotect import getkey

#  /* Function to scan protected docs against secure baseline stored in the db
#  * @return A JSON string  withe results of the baseline scan
#  */
def scandocs(db, BUF_SIZE, alert):
    # retrieve docs of type doc
    items = []
    query = Query(db, selector={'type': {'$eq': 'doc'}, 'status': {'$eq': 1}}) # skip files reporting compromised state
# TODO handle already report compromised files

    print "scanning base-line..."

    status = 1
    for document in query.result:
        sha256 = hashlib.sha256()
# Generate the HMAC using the secure key stored in IBM Key-Protect
        digest = hmac.new(getkey(), '', hashlib.sha256)

        file = document['_id']
        if path.isfile(file):
            f = open(file, 'rb')
            # TODO add exception handling

            # Calculate an up to date HMAC for comparison
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

# JSON for reporting scan results
            data = {'host': document['host'],
                    'ipaddress': document['ipaddress'],
                    'file': document['_id']
                    }

# Check if base-line and latest HMAC are equal
# TODO as this is the key to everything, investigate further potential vulnerabilities and secure
            if digest.hexdigest() == document['hmac']:
                data['status'] = 1 # safe
            else:
                data['status'] = 2 # compromised
                status = 2
# If push notification alerts are enabled, send a alert
                if alert:
                    alert_slack(document['_id'], document['host'], document['ipaddress'])

            items.append(data)

# Update the bot doc in the db with the latest baseline scan status
        with Document(db, 'bot') as bot:
            bot['status'] = status

    return items