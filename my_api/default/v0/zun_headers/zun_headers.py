"""
header resource
"""
import uuid
from zunzuncito import tools


class APIResource(object):

    def dispatch(self, request, response):

        request.log.debug(tools.log_json({
            'API': request.version,
            'Method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        response.headers['naranjas'] = str(uuid.uuid4())

        return tools.log_json(response.headers, 4)
