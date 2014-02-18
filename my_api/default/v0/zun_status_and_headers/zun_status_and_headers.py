"""
status_and_headers resource
"""
from zunzuncito import tools


class APIResource(object):

    @tools.allow_methods('get')
    def dispatch(self, request, response):

        try:
            name = request.path[0]
        except Exception:
            name = ''

        if name:
            response.headers['my_custom_header'] = name
        else:
            response.status = 406

        return 'Name: ' + name
