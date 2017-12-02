#!/usr/bin/env python

import hashlib
import hmac
from os import path

from alert import alert_slack

def scanfiles(db, BUF_SIZE):
    for document in db:
        sha256 = hashlib.sha256()
        digest = hmac.new('secret-shared-key-goes-here', '', hashlib.sha256)
        file = document['file']
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

        print(document['file'])
        print('hash db> ' + document['hash'])
        print('hash fs> ' + sha256.hexdigest())
        print('hmac db> ' + document['hmac'])
        print('hmac fs> ' + digest.hexdigest())

        if digest.hexdigest() == document['hmac']:
            print "match"
        else:
            print "data does not match"
            alert_slack(document['file'], document['host'], document['ipaddress'])