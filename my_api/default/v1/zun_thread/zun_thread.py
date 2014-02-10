"""
print the environ dict
"""


from zunzuncito import tools


class APIResource(object):

    def __init__(self):
        self.headers = {'Content-Type': 'text/html; charset=UTF-8'}

    def dispatch(self, request):

        request.log.info(tools.log_json({
            'API': request.version,
            'URI': request.URI,
            'rid': request.request_id,
            'in': 'dispatch',
            'thread': request.environ.get('thread', '-'),
        }))

        request.headers.update(self.headers)

        return tools.log_json(request.environ, 4)
