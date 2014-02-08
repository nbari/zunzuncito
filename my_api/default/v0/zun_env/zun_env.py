"""
print the environ dict
"""

import logging
import time

from zunzuncito import tools


class APIResource(object):

    def __init__(self, req):
        self.req = req
        self.log = req.log
        self.log.debug(tools.log_json({
            'API': req.version,
            'URI': req.URI,
            'rid': req.request_id,
            'vroot': req.vroot,
            'tread': req.environ['thread']
        }, True))
        self.req.headers['content-TyPe'] = 'text/html; charset=UTF-8'

    def dispatch(self, environ):

        # self.req.headers['content-TyPe'] = 'text/html; charset=UTF-8'

        self.log.info(tools.log_json({
            'rid': self.req.request_id,
            'thread_init': self.req.environ['thread'],
            'thread_func': environ['thread']
        }))

        time.sleep(1)

        return tools.log_json(environ, 4)
