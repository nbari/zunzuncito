"""
v0 ip_tools resource
"""

from zunzuncito import tools


class APIResource(object):

    @tools.allow_methods('get')
    def dispatch(self, request, response):
        request.log.debug(tools.log_json({
            'API': request.version,
            'Method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        data = {}

        try:
            my_ip = True if request.path[0] == 'ip' else False
        except Exception:
            my_ip = False

        if my_ip:
            data['ip'] = request.environ.get('REMOTE_ADDR', 0)
        else:
            data['API'] = request.version
            data['ip'] = request.environ.get('REMOTE_ADDR', 0)
            data['URI'] = request.URI
            data['method'] = request.method
            data['city'] = request.environ.get('HTTP_X_APPENGINE_CITY', 0)
            data['latlong'] = request.environ.get(
                'HTTP_X_APPENGINE_CITYLATLONG', 0)
            data['country'] = request.environ.get(
                'HTTP_X_APPENGINE_COUNTRY', 0)

        return tools.log_json(data, 4)
