"""
http_status/200/ resource
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

        data = {}
        data['path'] = request.path
        data['API'] = request.version,
        data['Method'] = request.method,
        data['URI'] = request.URI,
        data['vroot'] = request.vroot

        return tools.log_json(data, 4)
