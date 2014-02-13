"""
jinja2 resource
"""

import os

from jinja2 import Environment, FileSystemLoader
from zunzuncito import tools

jinja = Environment(autoescape=True, loader=FileSystemLoader(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')))


class APIResource(object):

    def __init__(self):
        self.headers = {'Content-Type': 'text/html; charset=UTF-8'}

    def dispatch(self, request, response):
        request.log.debug(tools.log_json({
            'API': request.version,
            'method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        response.headers.update(self.headers)


        template_values = {
            'IP': request.environ.get('REMOTE_ADDR', 0)
        }

        template = jinja.get_template('example.html')

        return template.render(template_values).encode('utf-8')
