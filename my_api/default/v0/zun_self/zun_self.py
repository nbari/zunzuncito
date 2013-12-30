"""
default resource
"""
import json
import logging
from zunzuncito import tools
from zunzuncito import http_status_codes


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = api.headers.copy()
        self.log = logging.getLogger()
        self.log.info(tools.log_json({
            'vroot': api.vroot,
            'API': api.version,
            'URI': api.URI,
            'method': api.method
        }, True)
        )

    @tools.allow_methods('get')
    def dispatch(self, environ, start_response):
        headers = self.api.headers
        start_response(
            getattr(http_status_codes, 'HTTP_%d' %
                    self.status), list(headers.items()))

        return (
            json.dumps(
                tools.clean_dict(self.api.__dict__),
                sort_keys=True,
                indent=4)
        )