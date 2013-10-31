"""
default resource
"""
import json
from zunzuncito.exceptions import MethodException, HTTPException, allow


class APIResource(object):

    def __init__(self, app):
        self.app = app
        self.status = 200
        self.headers = {}

    @allow('get', 'post')
    def dispatch(self):
        return 'ja quase'
