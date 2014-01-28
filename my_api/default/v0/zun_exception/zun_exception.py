"""
test HTTP exceptions
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
            raise tools.HTTPException(400)

        if name != 'foo':
            raise tools.HTTPException(
                406,
                title='exeption example',
                description='name must be foo',
                code='my-custom-code',
                display=True)

        return __name__
