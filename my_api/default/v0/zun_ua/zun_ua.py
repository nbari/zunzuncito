"""
print the environ dict
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

        b = request.environ.get('HTTP_USER_AGENT')

        for k, v in request.environ.items():
            # convert all string values to unicode values and replace
            # malformed data with a suitable
            # replacement marker.
            if isinstance(v, str):
                request.environ[k] = v.decode('utf-8', 'replace')

        a = request.environ.get('HTTP_USER_AGENT')
        return str(type(b)) + str(type(a))
