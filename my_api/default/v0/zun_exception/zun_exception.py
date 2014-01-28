"""
test HTTP exceptions
"""
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

    @tools.allow_methods('get')
    def dispatch(self, environ):

        try:
            name = self.api.path[0]
        except:
            raise tools.HTTPException(400)

        if name != 'foo':
            raise tools.HTTPException(
                406,
                title='exeption example',
                description='name must be foo',
                code='my-custom-code',
                display=True)

        return __name__
