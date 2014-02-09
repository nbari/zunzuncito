"""
print the environ dict
"""

import logging

from zunzuncito import tools


class APIResource(object):

    def __init__(self, req):
        self.req = req
        self.log = req.log
        self.log.info(tools.log_json({
            'API': req.version,
            'URI': req.URI,
            'rid': req.request_id,
            'in': '__init__',
            'thread': req.environ.get('thread', 0)
        }))
        self.req.headers['content-TyPe'] = 'text/html; charset=UTF-8'

    def dispatch(self, environ):

        self.log.info(tools.log_json({
            'API': self.req.version,
            'URI': self.req.URI,
            'rid': self.req.request_id,
            'in': 'dispatch',
            'thread': self.req.environ.get('thread', '-'),
            'thread_env': environ.get('thread', '-')
        }))

        return tools.log_json(environ)