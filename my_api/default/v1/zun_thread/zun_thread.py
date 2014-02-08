"""
print the environ dict
"""

import logging

from zunzuncito import tools


class APIResource(object):

    def __init__(self, log, req):
        self.log = log
        self.req = req

    def __call__(self, req):
        self.req = req
        self.log.info(tools.log_json({
            'API': req.version,
            'URI': req.URI,
            'rid': req.request_id,
            'in': '__call__',
            'thread': req.environ['thread']
        }))

    def dispatch(self, environ):

        # self.req.headers['content-TyPe'] = 'text/html; charset=UTF-8'

        self.log.info(tools.log_json({
            'API': self.req.version,
            'URI': self.req.URI,
            'rid': self.req.request_id,
            'in': 'dispatch',
            'thread': self.req.environ.get('thread', '-'),
            'thread_env': environ.get('thread', '-')
        }))

        return tools.log_json(environ, 4)
