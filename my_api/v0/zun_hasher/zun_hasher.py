"""
hasher API resource
"""
import hashlib
import json
import logging
from zunzuncito import http_status_codes
from zunzuncito.tools import MethodException, HTTPException, allow_methods


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = api.headers.copy()
        self.log = logging.getLogger()
        self.log.setLevel('INFO')
        self.log = logging.LoggerAdapter(
            logging.getLogger(), {
                'rid': api.request_id,
                'indent': 4
            })
        self.log.info(dict((x, y) for x, y in (
            ('API', api.version),
            ('URI', api.URI),
            ('method', api.method)
        )))

    @allow_methods('get')
    def dispatch(self, environ, start_response):
        headers = self.api.headers
        start_response(
            getattr(http_status_codes, 'HTTP_%d' %
                    self.status), list(headers.items()))


        hash_type = self.api.resource
        string = ''.join(self.api.path[:1])

        data = {}
        data['type'] = hash_type
        data['string'] = string

        if hash_type == 'md5':
            data['hash'] = hashlib.md5(string).hexdigest()
        elif hash_type == 'sha1':
            data['hash'] = hashlib.md5(string).hexdigest()
        elif hash_type == 'sha256':
            data['hash'] = hashlib.sha256(string).hexdigest()
        elif hash_type == 'sha512':
            data['hash'] = hashlib.sha512(string).hexdigest()

        return json.dumps(data, sort_keys=True, indent=4)
