"""
ip_tools resource
"""
import json
import logging

from zunzuncito import tools


class APIResource(object):

    def __init__(self, api):
        self.api = api

    @tools.allow_methods('get')
    def dispatch(self, environ):

        data = {}

        try:
            my_ip = True if self.api.path[0] == 'ip' else False
        except:
            my_ip = False

        if my_ip:
            data['ip'] = environ.get('REMOTE_ADDR', 0)
        else:
            data['API'] = self.api.version
            data['ip'] = environ.get('REMOTE_ADDR', 0)
            data['URI'] = self.api.URI
            data['method'] = self.api.method
            data['city'] = environ.get('HTTP_X_APPENGINE_CITY', 0)
            data['latlong'] = environ.get('HTTP_X_APPENGINE_CITYLATLONG', 0)
            data['country'] = environ.get('HTTP_X_APPENGINE_COUNTRY', 0)

        return tools.log_json(data, 4)
