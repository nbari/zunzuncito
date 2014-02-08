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
            'tread': req.environ['thread']
        }, True))

    def __call__(self, req):
        self.req = req
        self.log.info(tools.log_json({
            'API': req.version,
            'URI': req.URI,
            'rid': req.request_id,
            'in': '__call__',
            'tread': req.environ['thread']
        }, True))

    def dispatch(self, environ):

        # self.req.headers['content-TyPe'] = 'text/html; charset=UTF-8'

        self.log.info(tools.log_json({
            'rid': self.req.request_id,
            'thread_me': self.req.environ['thread'],
            'thread_env': environ['thread']
        }))

        return tools.log_json(environ, 4)
