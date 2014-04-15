"""
handles the response
"""

from zunzuncito import http_status_codes
from zunzuncito import tools


class Response(object):

    def __init__(self, logger, request_id, headers, start_response):
        self.log = logger
        self.headers = headers
        self.request_id = request_id
        self.status = 200
        self.start_response = start_response
        self.extra = []

    def get_status(self):

        try:
            status = int(self.status)
        except Exception as e:
            self.log.error(
                tools.log_json({'no status': e, 'status': self.status}))
            status = 500

        try:
            if status in http_status_codes.codes:
                status = http_status_codes.codes[status]
            else:
                status = http_status_codes.generic_reasons[status // 100]
        except Exception as e:
            self.log.error(tools.log_json({'bad status': e, 'status': status}))
            status = '500 Internal Server Error'

        return status

    def get_headers(self):

        if 'content-type' not in self.headers:
            self.headers['Content-Type'] = 'application/json; charset=UTF-8'

        self.headers['Request-ID'] = self.request_id

        return list(self.headers.items() + self.extra)

    def send(self):
        self.start_response(self.get_status(), self.get_headers())

    def add_header(self, name, value):
        header = (name, value)
        self.extra.append(header)

    def __str__(self):
        return '\r\n'.join(
            ['%s: %s' % v for v in self.headers.items() + self.extra])
