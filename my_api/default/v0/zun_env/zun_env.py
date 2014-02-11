"""
print the environ dict
"""

from zunzuncito import tools


class APIResource(object):

    def __call__(self, response):
        # response headers
        pass

    def headers(self, response):
        # response headers
        pass


    def dispatch(self, request, response):

        request.log.debug(tools.log_json({
            'API': request.version,
            'Method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        return tools.log_json(request.environ, 4)
