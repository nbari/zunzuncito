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
        self.log = logging.LoggerAdapter(logging.getLogger(),{'rid': api.request_id, 'indent': 4})

    @allow_methods('get', 'post')
    def dispatch(self, environ, start_response):
        headers = self.api.headers
        start_response(getattr(http_status_codes, 'HTTP_%d' % 201), list(headers.items()))
        print '------xxxx-------'
        #self.log.debug({k: v for k, v in self.api.__dict__.items() if v})
        return __name__
