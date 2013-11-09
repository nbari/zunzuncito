"""
default resource
"""
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
        data = {}
        data['API'] = self.api.version
        data['REMOTE_ADDR'] = environ.get('REMOTE_ADDR', 0)
        data['URI'] = self.api.URI
        data['method'] = self.api.method
        data['city'] = environ.get('HTTP_X_APPENGINE_CITY', 0)
        data['latlong'] = environ.get('HTTP_X_APPENGINE_CITYLATLONG', 0)
        data['country'] = environ.get('HTTP_X_APPENGINE_COUNTRY', 0)

        return json.dumps(data, sort_keys=True, indent=4)
