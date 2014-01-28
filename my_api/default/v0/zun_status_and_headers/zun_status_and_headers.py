"""
status_and_headers resource
"""
from zunzuncito import tools


class APIResource(object):

    def __init__(self, api):
        self.api = api

    @tools.allow_methods('get')
    def dispatch(self, environ):

        try:
            name = self.api.path[0]
        except:
            name = ''

        if name:
            self.api.headers['my_custom_header'] = name
        else:
            self.api.status = 406

        return 'Name: ' + name
