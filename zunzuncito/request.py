"""
handles the request
"""

from zunzuncito import http_status_codes
from zunzuncito import tools


class Request(object):

    def __init__(self, logger, request_id, environ, headers):
        self.log = logger
        self.request_id = request_id
        self.environ = environ
        self.headers = headers
        self.URI = '/'
        self.host = None
        self.method = environ['REQUEST_METHOD']
        self.path = []
        self.resource = None
        self.status = 200
        self.version = None
        self.vroot = 'default'

        """
        set the HOST
        """
        if 'HTTP_HOST' in environ:
            self.host = environ['HTTP_HOST'].split(':')[0]

        """
        set the request URI
        """
        if 'REQUEST_URI' in environ:
            self.URI = environ['REQUEST_URI']
        elif 'PATH_INFO' in environ:
            self.URI = environ['PATH_INFO']

    def response(self, start_response):

        status = self.status

        try:
            status = int(status)
        except Exception as e:
            self.log.error(tools.log_json({'no status': e, 'status': status}))
            status = 500

        try:
            if status in http_status_codes.codes:
                status = http_status_codes.codes[status]
            else:
                status = http_status_codes.generic_reasons[status // 100]
        except Exception as e:
            self.log.error(tools.log_json({'bad status': e, 'status': status}))
            status = '500 Internal Server Error'

        if not 'content-type' in self.headers:
            self.headers['Content-Type'] = 'application/json; charset=UTF-8'

        self.headers['Request-ID'] = self.request_id

        start_response(status, list(self.headers.items()))
