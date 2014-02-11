"""
static resource
"""
from zunzuncito import tools


class APIResource(object):

    @tools.allow_methods('get, head')
    def dispatch(self, request, response):

        data = {
            'URI': request.URI,
            'resource': request.resource,
            'path': request.path,
        }
        return tools.log_json(data, 4)
