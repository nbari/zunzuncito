"""
unicode resource
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

    @tools.allow_methods('get, post')
    def dispatch(self, environ):

        data = {}
        if environ.get('CONTENT_TYPE', '').startswith('multipart'):
            data['files'] = True

        return tools.log_json(data, 4)
