"""
print the environ dict
"""


from zunzuncito import tools


class APIResource(object):

    def __init__(self):
        self.headers = {'Content-Type': 'text/html; charset=UTF-8'}

    def dispatch(self, req, res):

        req.log.info(tools.log_json({
            'API': req.version,
            'URI': req.URI,
            'rid': req.request_id,
            'in': 'dispatch',
            'thread': req.environ.get('thread', '-'),
        }))

        res.headers.update(self.headers)
        res.body = tools.log_json(req.environ, 4)
