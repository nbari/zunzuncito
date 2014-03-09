"""
/get/client/ resource
"""

from zunzuncito import tools


class APIResource(object):

    def dispatch(self, request, response):

        request.log.debug(tools.log_json({
            'API': request.version,
            'Method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        return __name__
