"""
Main class
"""

import exceptions
import constants
import os
import urlparse


class ZunZun(object):

    def __init__(self, document_root=None):
        if document_root:
            self.document_root = os.path.abspath(document_root)
            if not os.access(self.document_root, os.R_OK):
                raise Exception('Document root not readable')
        else:
            raise Exception('Document root missing')
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
            status, headers, body = self.dispatch()
        except MethodExcept, e:
            pass
        except HTTPExcept, e:
            pass

#        status, headers, body = router(self.method, self.request_URI, self.params, self.env)

        status = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]

        start_response(status, headers)
        return str(body)


    def dispatch(self):
        """
        find resource module/comand/args "a la SlashQuery"
        """
        resource = [x.strip() for x in self.request_URI.split('/') if x]
        return (None, None, resource)



    def add_route(self, route=None):
        pass
