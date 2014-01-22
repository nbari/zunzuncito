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
        data = {}
        data['about'] = ("Hi %s, I am zunzuncito a micro-framework for creating"
                         " REST API's, you can read more about me in: "
                         "www.zunzun.io") % environ.get('REMOTE_ADDR', 0)

        data['Request-ID'] = self.api.request_id
        data['URI'] = self.api.URI
        data['Method'] = self.api.method

        return tools.log_json(data, 4)
