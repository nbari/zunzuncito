"""
webob resource
"""

from webob import Request
from zunzuncito import tools


class APIResource(object):

    def dispatch(self, request, response):
        req = Request(request.environ)

        # to get a post param
        # field = req.POST['field']

        data = {}
        data['req-GET'] = req.GET
        data['req-POST'] = req.POST
        data['req-application_url'] = req.application_url
        data['req-body'] = req.body
        data['req-content_type'] = req.content_type
        data['req-cookies'] = req.cookies
        data['req-method'] = req.method
        data['req-params'] = req.params
        data['req-path'] = req.path
        data['req-path_info'] = req.path_info
        data['req-path_qs'] = req.path_qs
        data['req-path_url'] = req.path_url
        data['req-query_string'] = req.query_string
        data['req-script_name'] = req.script_name
        data['req-url'] = req.url

        return tools.log_json(data, 4)
