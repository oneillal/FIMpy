#!/usr/bin/env python

import hashlib
import hmac
from os import path

from cloudant.query import Query
from cloudant.document import Document
from alert import alert_slack
from ibmkeyprotect import getkey


def scandocs(db, BUF_SIZE, alert):
    # retrieve docs of type proof
    items = []
    query = Query(db, selector={'type': {'$eq': 'doc'}, 'status': {'$eq': 1}}) # skip files reporting compromised state

    print "scanning..."

    status = 1
    for document in query.result:
        sha256 = hashlib.sha256()
        digest = hmac.new(getkey(), '', hashlib.sha256)
        file = document['_id']
        if path.isfile(file):
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

            # print(document['file'])
            # print('hash db> ' + document['hash'])
            # print('hash fs> ' + sha256.hexdigest())
            # print('hmac db> ' + document['hmac'])
            # print('hmac fs> ' + digest.hexdigest())

            data = {'host': document['host'],
                    'ipaddress': document['ipaddress'],
                    'file': document['_id']
                    }

            if digest.hexdigest() == document['hmac']:
                data['status'] = 1 # safe
            else:
                data['status'] = 2 # compromised
                status = 2
                if alert:
                    alert_slack(document['_id'], document['host'], document['ipaddress'])

            items.append(data)

        with Document(db, 'bot') as bot:
            bot['status'] = status

    return items