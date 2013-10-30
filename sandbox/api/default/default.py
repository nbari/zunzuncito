"""
default resource
"""
import json


class Resource(object):

    def __init__(self, zunzun):
        self.zunzun = zunzun
        self.status = 200
        self.headers = {}

    def run(self):
        self.headers['Content-Type'] = 'application/json; charset=utf-8'
        return 'oioi'
