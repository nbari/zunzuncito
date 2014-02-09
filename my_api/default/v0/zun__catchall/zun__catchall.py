"""
catchall resource
"""

import logging

from zunzuncito import tools


class APIResource(object):

    def __init__(self, req):
        self.req = req
        self.log = req.log
        self.log.debug(tools.log_json({
            'API': req.version,
            'catchall': req.URI,
            'rid': req.request_id,
            'vroot': req.vroot
        }, True)
        )

    def __call__(self, req):
        self.req = req

    def dispatch(self, environ):

        return 'Hi ..' + str(self.req.path)
