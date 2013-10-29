"""
Main class
"""

import constants
import HTTPError
import urlparse

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
        self.request_URI = env['REQUEST_URI']

        """
        The portion of the request URL that follows the "?"
        """
        if 'QUERY_STRING' in env:
            self.params = urlparse.parse_qs(env['QUERY_STRING'])

        try:
            status, headers, body = self.dispatch(self.request_URI, self.method, self.params, self.env)
        except MethodError, e:
            pass
        except HTTPError, e:
            pass

        status, headers, body = router(self.method, self.request_URI, self.params, self.env)

        start_response(status, headers)
        return body

    def dispatch(self):
        """
        find module/comand/args
        """
        pass
