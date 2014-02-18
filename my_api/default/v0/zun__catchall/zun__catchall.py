"""
catchall resource
"""

from zunzuncito import tools


class APIResource(object):

    def dispatch(self, request, response):

        return 'Hi ..' + str(request.path)
