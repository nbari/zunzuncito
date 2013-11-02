"""
default resource
"""
import json
import logging
from zunzuncito.tools import MethodException, HTTPException, allow_methods


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = {}
        self.log = logging.LoggerAdapter(logging.getLogger(),
                {'rid': api.request_id, 'indent': 4})

    @allow_methods('get', 'post')
    def dispatch(self):
        print '------xxxx-------'
        self.log.debug({k: str(v) for k, v in self.api.__dict__.items() if v})
        return __name__
