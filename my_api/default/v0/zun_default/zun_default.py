"""
default resource
"""
from zunzuncito import tools


class APIResource(object):

    @tools.allow_methods('get, head')
    def dispatch(self, request, response):

        request.log.debug(tools.log_json({
            'API': request.version,
            'URI': request.URI,
            'method': request.method,
            'vroot': request.vroot
        }, True))

        data = {}
        data['about'] = ("Hi %s, I am zunzuncito a micro-framework for creating"
                         " REST API's, you can read more about me in: "
                         "www.zunzun.io") % request.environ.get('REMOTE_ADDR', 0)

        data['Request-ID'] = request.request_id
        data['URI'] = request.URI
        data['Method'] = request.method

        return tools.log_json(data, 4)
