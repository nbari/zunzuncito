"""
http_status resource
"""

from zunzuncito.http_status_codes import codes
from zunzuncito import tools


class APIResource(object):

    @tools.allow_methods('get')
    def dispatch(self, request, response):
        request.log.debug(tools.log_json({
            'API': request.version,
            'Method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        data = {}
        try:
            data['status code'] = codes[int(request.path[0], 0)]
        except Exception as _:
            data['status code'] = 'not found'

        data['URI'] = request.URI

        return tools.log_json(data, 4)
