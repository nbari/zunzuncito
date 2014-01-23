"""
default resource
"""
import logging
import uuid
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

    def dispatch(self, environ):

        self.api.headers['naranjas'] = str(uuid.uuid4())

        return tools.log_json(self.api.headers, 4)
