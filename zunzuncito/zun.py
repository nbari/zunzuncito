"""
Main class
"""

import constants
import urlparse
import json

class Zun(object):

    def __init__(self, content_type=constants.DEFAULT_CONTENT_TYPE):
        self.content_type = content_type
        self.routes = []

    def __call__(self, env, start_response):
        self.env = env

        """
        get the HTTP method
        """
        self.method = env['REQUEST_METHOD']

        """
        get the request URI
        """
        self.request_URL = env['REQUEST_URI']

        """
        The portion of the request URL that follows the "?"
        """
        if 'QUERY_STRING' in env:
            self.params = urlparse.parse_qs(env['QUERY_STRING'])


        yield json.dumps(self.params)
