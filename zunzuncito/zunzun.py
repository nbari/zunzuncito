"""
Main class
"""

import constants
import exceptions
import os
import re
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
        if 'REQUEST_URI' in env:
            self.URI = env['REQUEST_URI']
        elif 'PATH_INFO' in env:
            self.URI = env['PATH_INFO']
        else:
            self.URI = '/'

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
        resource = [x.strip() for x in self.URI.split('/') if x]
        if resource[0]:
            pass
            """ search on document root and import the module """
        else:
            pass
            """ load default """


        return (None, None, resource)



    def add_route(self, route=None):
        pass
