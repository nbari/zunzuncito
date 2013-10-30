"""
Main class
"""

import http_status_codes
import imp
import json
import os
import re
import urlparse
from exceptions import APIException


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

        status = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]

        try:
            request = self.dispatch()
            body = request.run()
            if hasattr(body, 'status'):
                status = getattr(http_status_codes, 'HTTP_%d' % body.status)
            if hasattr(body, 'headers'):
                headers = list(body.headers.items())
        except APIException, e:
            status = getattr(http_status_codes, 'HTTP_%d' % e.status)
            if e.headers:
                headers = list(e.headers.items())
            if e.title:
                body = e.to_json()
        except Exception, e:
            status = getattr(http_status_codes, 'HTTP_%d' % 500)
            body = 'Something is broken: ' + str(e)
           # body = json.dumps({k: str(env[k]) for k in env.keys()}, sort_keys=True, indent=4)

        start_response(status, headers)
        return body

    def dispatch(self):
        """
        find resource module/comand/args "a la SlashQuery"
        """
        resources = [x.strip() for x in self.URI.split('/') if x != 0]
        if resources[0]:
            module_path = os.path.join(self.document_root, '%s/%s.py' % (resources[0], resources[0]))
        else:
            module_path = os.path.join(self.document_root, 'default/default.py')

        if not os.access(module_path, os.R_OK):
            raise APIException(500, 'default module not readable')
        else:
            mod_name, file_ext = os.path.splitext(os.path.split(module_path)[-1])

            if file_ext == '.py':
                py_mod = imp.load_source(mod_name, module_path)
            elif file_ext == '.pyc':
                py_mod = imp.load_compiled(mod_name, module_path)

            return py_mod.Resource(self)

    def add_route(self, route=None):
        pass
