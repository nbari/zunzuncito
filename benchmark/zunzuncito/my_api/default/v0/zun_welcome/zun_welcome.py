"""
/welcome resource
"""


class APIResource(object):

    def __init__(self):
        self.headers = {'Content-Type': 'text/html; charset=UTF-8'}

    def dispatch(self, request, response):

        response.headers.update(self.headers)

        return ['Hello World!']
