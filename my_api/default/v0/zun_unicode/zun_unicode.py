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

        body = ''  # b'' for consistency on Python 3.0

        try:
            length = int(environ.get('CONTENT_LENGTH', '0'))
        except ValueError:
            length = 0

        if length != 0:
            body = environ['wsgi.input'].read(length)

        data = {}
        data['body'] = body

        if self.environ.get('CONTENT_TYPE', '').startswith('multipart'):
            data['files'] = True

        return tools.log_json(body, 4)
