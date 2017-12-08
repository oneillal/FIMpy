#!/usr/bin/env python
"""
FIMpy - A Python File Integrity Monitoring Application
"""

#########################################################################################
####################################  AUTH  #############################################
#########################################################################################
#                                                                                       #
#   Python module for authorisation functions using JumpCloud LDAP-as-a-Service         #
#                                                                                       #
#########################################################################################

__author__ = "Alan O'Neill"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Alan O'Neill"
__status__ = "Development"

import ldap
from functools import wraps
from flask import request, Response

def check_auth(username, password):
    return check_ldap(username, password)

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Authenticaton failed', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_ldap(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def check_ldap(user, pw):
# TODO store LDAP org-id in IBM Key-Protect
    dn = "uid=" + user + ",ou=Users,o=59fee5a1d7fed97c192c12ce,dc=jumpcloud,dc=com"
    server = "ldaps://ldap.jumpcloud.com:636"
    try:
        l = ldap.initialize(server)
        try:
            l.bind_s(dn, pw)
            return 1
        except ldap.INVALID_CREDENTIALS:
            return 0

        except ldap.LDAPError, e:
            print e
            return -1
    finally:
        l.unbind()