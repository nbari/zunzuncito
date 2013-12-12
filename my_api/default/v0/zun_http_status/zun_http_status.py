"""
default resource
"""
import json
import logging
from zunzuncito import http_status_codes
from zunzuncito.tools import MethodException, HTTPException, allow_methods


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = api.headers.copy()
        self.log = logging.getLogger()

    @allow_methods('get')
    def dispatch(self, environ, start_response):
        headers = self.api.headers
        start_response(
            getattr(http_status_codes, 'HTTP_%d' %
                    self.status), list(headers.items()))
        data = {}
        try:
            data['status code'] = getattr(
                http_status_codes, 'HTTP_%d' %
                int(self.api.resources[1], 0))
        except Exception as e:
            data['status code'] = 'not found'

        data['URI'] = self.api.URI

        return json.dumps(data, sort_keys=True, indent=4)
