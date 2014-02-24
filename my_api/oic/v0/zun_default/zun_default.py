"""
default resource
"""
from zunzuncito import tools


class APIResource(object):

    def dispatch(self, request, response):

        request.log.debug(tools.log_json({
            'API': request.version,
            'URI': request.URI,
            'method': request.method,
            'vroot': request.vroot
        }, True))

        return __name__
