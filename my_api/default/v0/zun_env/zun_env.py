"""
print the environ dict
"""
import json
import logging
from zunzuncito import tools


class APIResource(object):

    def __init__(self, api, head):
        self.api = api
        self.log = logging.getLogger()
        self.log.info(tools.log_json({
            'vroot': api.vroot,
            'API': api.version,
            'URI': api.URI
        }, True)
        )

    def dispatch(self, environ, start_response):

        return tools.log_json(environ, 4)
