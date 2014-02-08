"""
self resource
"""

import logging

from zunzuncito import tools


class APIResource(object):

    def __init__(self, req):
        self.req = req
        self.log = req.log
        self.log.info(tools.log_json({
            'vroot': req.vroot,
            'API': req.version,
            'URI': req.URI
        }, True)
        )

    def dispatch(self, environ, start_response):

#        tools.start_response(start_response, 200)
        return tools.log_json(self.req.__dict__, 4)
