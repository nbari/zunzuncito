"""
thread resource
"""

from zunzuncito import tools


class APIResource(object):

    def __init__(self):
        self.headers = {'content-TyPe': 'text/html; charset=UTF-8'}

    def dispatch(self, request, response):

        request.log.info(tools.log_json({
            'API': request.version,
            'URI': request.URI,
            'rid': request.request_id,
            'in': 'dispatch',
            'thread': request.environ.get('thread', '-'),
            'thread_env': request.environ.get('thread', '-')
        }))

        response.headers.update(self.headers)

        return tools.log_json(request.environ)
