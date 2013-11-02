"""
default resource
"""
import json
import logging
from zunzuncito.tools import MethodException, HTTPException, LogAdapter, allow_methods


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = {}
        self.log = LogAdapter(logging.getLogger(),
                              {'request_id': api.request_id,
                               'resource': __name__})

    @allow_methods('get', 'post')
    def dispatch(self):
        self.log.debug(json.dumps({k: str(v) for k, v in self.api.__dict__.items() if v},
                                  sort_keys=True,
                                  indent=4))
        return __name__
