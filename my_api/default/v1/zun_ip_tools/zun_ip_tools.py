"""
default resource
"""
import json
import logging
import socket
import struct
from zunzuncito import http_status_codes
from zunzuncito.tools import MethodException, HTTPException, allow_methods


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = api.headers.copy()

    @allow_methods('get')
    def dispatch(self, environ, start_response):
        headers = self.api.headers
        start_response(
            getattr(http_status_codes, 'HTTP_%d' %
                    self.status), list(headers.items()))
        data = {}
        try:
            my_ip = True if self.api.path[0] == 'ip' else False
        except:
            my_ip = False

        if my_ip:
            ip = environ.get('REMOTE_ADDR', 0)
            data['ip'] = ip
            data['inet_ntoa'] = struct.unpack("!I", socket.inet_aton(ip))[0]
        else:
            data['API'] = self.api.version
            data['ip'] = environ.get('REMOTE_ADDR', 0)
            data['URI'] = self.api.URI
            data['method'] = self.api.method
            data['city'] = environ.get('HTTP_X_APPENGINE_CITY', 0)
            data['latlong'] = environ.get('HTTP_X_APPENGINE_CITYLATLONG', 0)
            data['country'] = environ.get('HTTP_X_APPENGINE_COUNTRY', 0)

        return json.dumps(data, sort_keys=True, indent=4)
