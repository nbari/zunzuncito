"""
test HTTP exceptions
"""
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

        try:
            name = request.path[0]
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
