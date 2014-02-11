"""
hasher API resource
"""

import hashlib

from zunzuncito import tools


class APIResource(object):

    @tools.allow_methods('get, post')
    def dispatch(self, request, response):

        request.log.debug(tools.log_json({
            'API': request.version,
            'Method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        hash_type = request.resource

        if request.method == 'POST':
            string = ''

            try:
                length = int(request.environ.get('CONTENT_LENGTH', '0'))
            except ValueError:
                length = 0

            if length != 0:
                string = request.environ['wsgi.input'].read(length)
        else:
            string = '/'.join(request.path)

        data = {}
        data['type'] = hash_type
        data['string'] = string

        if hash_type == 'md5':
            data['hash'] = hashlib.md5(string).hexdigest()
        elif hash_type == 'sha1':
            data['hash'] = hashlib.sha1(string).hexdigest()
        elif hash_type == 'sha256':
            data['hash'] = hashlib.sha256(string).hexdigest()
        elif hash_type == 'sha512':
            data['hash'] = hashlib.sha512(string).hexdigest()

        return tools.log_json(data, 4)
