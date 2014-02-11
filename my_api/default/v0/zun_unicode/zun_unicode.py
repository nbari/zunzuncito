"""
unicode resource
"""
import uuid
from zunzuncito import tools


class APIResource(object):

    @tools.allow_methods('get, post')
    def dispatch(self, request, response):
        request.log.debug(tools.log_json({
            'API': request.version,
            'Method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        data = {}
        if request.environ.get('CONTENT_TYPE', '').startswith('multipart'):
            data['files'] = True

        return tools.log_json(data, 4)
