"""
default resource
"""
import logging
from zunzuncito import tools


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.log = logging.getLogger()
        self.log.info(tools.log_json({
            'vroot': api.vroot,
            'API': api.version,
            'URI': api.URI,
            'method': api.method
        }, True)
        )

    @tools.allow_methods('get, head')
    def dispatch(self, environ):

        data = {
            'URI': self.api.URI,
            'resource': self.api.resource,
            'path': self.api.path,
        }
        return tools.log_json(data, 4)
