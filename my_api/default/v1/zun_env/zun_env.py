"""
v1 print the environ dict
"""

from zunzuncito import tools


class APIResource(object):

    def dispatch(self, request, response):

        return tools.log_json(request.environ, 4)
