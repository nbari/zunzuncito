"""
default resource
"""
import json
import logging
from zunzuncito.tools import MethodException, HTTPException, logAdapter, allow_methods

log = logAdapter(logging.getLogger(), {'py_mod': __name__})


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = {}
        log.debug('i am: %s', __name__)

    @allow_methods('get', 'post')
    def dispatch(self):
        log.debug(__name__)
        return __name__
