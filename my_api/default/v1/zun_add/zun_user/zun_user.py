"""
v1 add/user resource
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
        data['URI'] = request.URI
        data['py_mod'] = request.py_mod
        data['path'] = request.path

        return tools.log_json(data, 4)
