"""
http_status resource
"""
import logging
from zunzuncito.http_status_codes import codes
from zunzuncito import tools


class APIResource(object):

    def __init__(self, api):
        self.api = api
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
    def dispatch(self, environ):

        data = {}
        try:
            data['status code'] = codes[int(self.api.path[0], 0)]
        except Exception as e:
            data['status code'] = 'not found'

        data['URI'] = self.api.URI

        return tools.log_json(data, 4)
