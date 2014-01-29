"""
jinja2 resource
"""

import logging
import os

from jinja2 import Environment, FileSystemLoader
from zunzuncito import tools

jinja = Environment(autoescape=True, loader=FileSystemLoader(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates')))


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.log = logging.getLogger()
        self.log.info(tools.log_json({
            'vroot': api.vroot,
            'API': api.version,
            'URI': api.URI,
            'method': api.method
        }, True)
        )

    def dispatch(self, environ):

        self.api.headers['Content-Type'] = 'text/html; charset=UTF-8'

        template_values = {
            'IP': environ.get('REMOTE_ADDR', 0)
        }

        template = jinja.get_template('example.html')

        return template.render(template_values).encode('utf-8')
