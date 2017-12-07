#!/usr/bin/env python

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