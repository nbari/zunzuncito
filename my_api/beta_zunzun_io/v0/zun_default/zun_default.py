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

        data = {}
        data['about'] = "Hi %s, I am %s on %s" % (
            request.environ.get('REMOTE_ADDR',
                                0),
            request.host,
            request.vroot)

        data['Method'] = request.method
        data['Request-ID'] = request.request_id
        data['URI'] = request.URI
        data['host'] = request.host
        data['vroot'] = request.vroot

        return tools.log_json(data, 4)
