"""
self resource
"""

from zunzuncito import tools


class APIResource(object):

    def dispatch(self, request, response):

        return tools.log_json(request.__dict__, 4)
