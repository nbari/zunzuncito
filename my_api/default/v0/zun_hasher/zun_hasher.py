"""
hasher API resource
"""
import hashlib
import json
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

    @tools.allow_methods('get, post')
    def dispatch(self, environ):

        hash_type = self.api.resource

        if self.api.method == 'POST':
            string = ''

            try:
                length = int(environ.get('CONTENT_LENGTH', '0'))
            except ValueError:
                length = 0

            if length != 0:
                string = environ['wsgi.input'].read(length)
        else:
            string = '/'.join(self.api.path)

        data = {}
        data['type'] = hash_type
        data['string'] = string

        if hash_type == 'md5':
            data['hash'] = hashlib.md5(string).hexdigest()
        elif hash_type == 'sha1':
            data['hash'] = hashlib.sha1(string).hexdigest()
        elif hash_type == 'sha256':
            data['hash'] = hashlib.sha256(string).hexdigest()
        elif hash_type == 'sha512':
            data['hash'] = hashlib.sha512(string).hexdigest()

        return json.dumps(data, sort_keys=True, indent=4)
