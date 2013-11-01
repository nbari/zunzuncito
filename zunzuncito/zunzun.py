"""
ZunZuncito

micro-framework for creating REST API's
"""

import http_status_codes
import imp
import json
import logging
import os
import re
import urlparse
from itertools import ifilter
from tools import HTTPError, MethodException, HTTPException


class ZunZun(object):

    def __init__(self, document_root=None, routes=None, suffix='zun', debug=False):
        if document_root:
            self.document_root = os.path.abspath(document_root)
            if not os.access(self.document_root, os.R_OK):
                raise Exception('Document root not readable')
        else:
            raise Exception('Document root missing')

        self.resources = []
        self.routes = []
        self.suffix = suffix

        """
        set the logger
        """
        self.log = logging.getLogger()

        handler = logging.FileHandler('%s/debug.log' % self.document_root)
        formatter = logging.Formatter('%(asctime)s [%(name)s - %(levelname)s] > %(message)s')
        handler.setFormatter(formatter)

        self.log.addHandler(handler)
        self.log.setLevel('DEBUG' if debug else 'ERROR')

        """
        register / compile the routes regex
        """
        if routes:
            self.register_routes(routes)

    def __call__(self, env, start_response):
        """
        try to be compliant with pep 3333 so that any WSGI can serve the app
        """
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

        """
        if debug, log the full environ
        """
        self.log.debug(json.dumps({k: str(env[k]) for k in env}, sort_keys=True, indent=4))

        """
        Default values
        """
        status = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        body = ''

        try:
            resource = self.router()
            body = resource.dispatch()

            if hasattr(body, 'status'):
                status = getattr(http_status_codes, 'HTTP_%d' % body.status)

            if hasattr(body, 'headers'):
                headers = list(body.headers.items())

        except HTTPError, e:
            status = getattr(http_status_codes, 'HTTP_%d' % e.status)

            if e.headers:
                headers = list(e.headers.items())

            if e.title:
                body = e.to_json()

            self.log.debug('HTTPError - %s [URI: %s]: %s', status, self.URI, e.to_json())

        except Exception, e:
            self.log.error('env: %s, exception: %s', json.dumps({k: str(env[k]) for k in env.keys()}, sort_keys=True, indent=4), e)
            status = getattr(http_status_codes, 'HTTP_%d' % 500)

        start_response(status, headers)
        return body

    def router(self):
        """
        first try to match any supplied routes (regex match)
        second find API resource /py_mod/command/args 'a la SlashQuery'
        """

        py_mod = False

        """
        t[0] = regex
        t[1] = module
        t[2] = data
        """
        filterf = lambda t: any(i in (self.method.upper(), 'ALL') for i in t[2])
        for regex, module, method in ifilter(filterf, self.routes):
            match = regex.match(self.URI)
            if match:
                py_mod = module
                self.log.debug('router - regex match: %s', json.dumps({'regex': regex,
                                                                       'URI': self.URI,
                                                                       'HTTP method': method}, indent=4))
                continue

        if not py_mod:
            self.resources = [x.strip() for x in self.URI.split('?')[0].split('/') if x]

            if not self.resources:
                py_mod = 'default'
            else:
                py_mod = self.resources[0]

        """
        by default the _zun suffix is appended, this is to avoid posible
        conflicts, example if you want to have a module call 'gevent' the
        directory structure should be gevent_zun/gevent_zun.py, the URI:
        http://yourapi.tld/gevent/
        you can change the suffix when starting the class
        see PEP: 395
        """
        py_mod = py_mod.lower()
        module_path = os.path.join(self.document_root, '%s_%s/%s_%s.py' % (py_mod, self.suffix, py_mod, self.suffix))

        if not os.access(module_path, os.R_OK):
            self.log.error('router - py_mod: %s not readable', py_mod)
            raise HTTPException(500, title="[ %s ] module not readable" % py_mod)
        else:
            mod_name, file_ext = os.path.splitext(os.path.split(module_path)[-1])

            py_mod = imp.load_source(mod_name, module_path)

            try:
                self.log.debug('router - dispatching(%s, %s)', mod_name, module_path)
                return py_mod.APIResource(self)
            except:
                raise HTTPException(500, title="[ %s ] missing APIResource class" % mod_name)

    def register_routes(self, routes):
        """compile regex pattern for routes

        :param routes:
            tuple(regex, handler, methods).
        """
        if routes:
            for route in routes:
                if isinstance(route, tuple):
                    regex, module = route[:2]
                    methods = ['ALL']

                    if len(route) > 2:
                        methods = [x.strip().upper() for x in route[2].split(',') if x]

                    if regex.startswith('^'):
                        self.routes.append((re.compile(regex), module, methods))
                    else:
                        self.routes.append((re.compile('^%s$' % regex), module, methods))

                    self.log.debug('registering route: %s', json.dumps({'regex': regex,
                                                                        'module': module,
                                                                        'methods': methods}, indent=4))
