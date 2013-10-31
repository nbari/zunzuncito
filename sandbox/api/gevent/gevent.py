"""
default resource
"""
import json
from zunzuncito.exceptions import MethodException, HTTPException, allow


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = {}

    def dispatch(self):
        return __name__
