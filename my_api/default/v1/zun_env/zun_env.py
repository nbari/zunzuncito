"""
print the environ dict
"""

import logging

from zunzuncito import tools


class APIResource(object):

    def __init__(self, req):
        self.req = req
        self.log = req.log
        self.log.debug(tools.log_json({
            'API': req.version,
            'URI': req.URI,
            'rid': req.request_id,
            'vroot': req.vroot
        }, True)
        )

    def __call__(self, req):
        self.req = req

    def dispatch(self, environ):

        self.log.info(tools.log_json({'rid': self.req.request_id}))

        return tools.log_json(environ, 4)
