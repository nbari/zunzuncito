"""
v1 add resource
"""

from zunzuncito import tools


class APIResource(object):

    def dispatch(self, request, response):

        data = {}
        data['URI'] = request.URI
        data['py_mod'] = request.py_mod
        data['path'] = request.path

        return tools.log_json(data, 4)
