# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


#########################################################################################
####################################  AUTH  #############################################
#########################################################################################
#                                                                                       #
#   This sample code was downloaded from IBM Key-Protect's repo on GiHub and adapted    #
#   in order to obtain a key from the key repository to generate a secure HMAC          #
#                                                                                       #
#   Reference: https://github.com/IBM-Bluemix/key-protect-helloworld-python             #
#                                                                                       #
#########################################################################################


from __future__ import print_function
import sys

import os
import requests
from flask import jsonify
import json

route_secrets = '/api/v2/keys'
authorization_header_field = 'Authorization'
space_header_field = 'Bluemix-Space'
org_header_field = 'Bluemix-Org'
secret_mime_type = 'application/vnd.ibm.kms.secret+json'
aes_algorithm_type = 'AES'

def setup():
    if os.path.isfile('vcap-local.json'):
        with open('vcap-local.json') as f:
            vcap = json.load(f)
            cred = vcap['services']['ibmKeyProtect'][0]
            url = 'https://' + cred['host'] + route_secrets
            token = cred['token'].strip()
            space = cred['space'].strip()
            org = cred['org'].strip()
            headers = {
                'Content-Type': 'application/json',
                authorization_header_field: token.encode('UTF-8'),
                space_header_field: space.encode('UTF-8'),
                org_header_field: org.encode('UTF-8')
            }

    return url, headers


def getkey():
# My FIMpy key reference id
    key_id = '5f715b2b-1809-4f88-ade7-69845b02ea34'

    url, headers = setup()
    key_url = '/'.join([url, key_id])

    try:
        get_key_request = requests.get(key_url, headers=headers)

        get_key_status = get_key_request.status_code
        response_key = get_key_request.json()

        if get_key_status >= 400:
            raise Exception(get_key_status, response_key)

        payload_key = response_key['resources'][0]['payload'].encode('UTF-8')
        return payload_key

    except requests.exceptions.RequestException as e:
        print('\n\n'+str(e), file=sys.stderr)
        err_msg = 'Cannot get key'
        response = jsonify(message=err_msg)
        response.status_code = 400
        return response
    except Exception as e:
        print('\n\n'+str(e), file=sys.stderr)
        response = jsonify(message=e.message, key_id=key_id)
        response.status_code = 400
        return response
