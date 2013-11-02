"""
test_upload resource
"""
import cgi
import cgitb
import json
import logging
from pprint import pformat
from zunzuncito import http_status_codes
from zunzuncito.tools import MethodException, HTTPException, allow_methods


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.headers = api.headers.copy()
        self.log = logging.LoggerAdapter(logging.getLogger(),{'rid': api.request_id, 'indent': 4})

    @allow_methods('get', 'post')
    def dispatch(self, environ, start_response):
        # self.log.debug({k: v for k, v in self.api.__dict__.items() if v})
        #post_env = self.api.env.copy()
        #post_env['QUERY_STRING'] = ''
        #form = cgi.FieldStorage(fp = self.api.env['wsgi.input'], environ=post_env)
        #print form
        #yield form
       # show the environment:
        output = ['<pre>']
        output.append('<h1>FORM DATA</h1>')
        output.append(pformat(environ['wsgi.input'].read()))

        # send results
        output_len = sum(len(line) for line in output)

#        raise HTTPException(201)

        self.headers['Content-Type'] = 'text/html'
        self.headers['Content-Length'] = str(output_len)

#        raise HTTPException(201)

        start_response(getattr(http_status_codes, 'HTTP_%d' % 200), list(self.headers.items()))

#        raise HTTPException(405)
        return output
        #print self.api.headers
        #return str(self.api.headers)
