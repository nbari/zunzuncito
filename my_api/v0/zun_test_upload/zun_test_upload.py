"""
test_upload resource
"""
import io
import logging
import os
from zunzuncito import http_status_codes
from zunzuncito.tools import MethodException, HTTPException, allow_methods


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = api.headers.copy()
        self.log = logging.getLogger()
        # self.log.setLevel('DEBUG')
        self.log.setLevel('INFO')
        self.log = logging.LoggerAdapter(
            logging.getLogger(), {
                'rid': api.request_id,
                'indent': 4
            })
        self.log.info(dict((x, y) for x, y in (
            ('API', api.version),
            ('URI', api.URI),
            ('method', api.method)
        )))

    @allow_methods('post', 'path', 'put')
    def dispatch(self, environ, start_response):
        try:
            temp_name = self.api.resources[1]
        except:
            raise HTTPException(400)

        """rfc2616-sec14.html
        see http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        see http://www.grid.net.ru/nginx/resumable_uploads.en.html

        """
        content_range = environ.get('HTTP_CONTENT_RANGE', 0)

        length = int(environ.get('CONTENT_LENGTH', 0))

        if content_range:
            content_range = content_range.split()[1].split('/')

            index, offset = [int(x) for x in content_range[0].split('-')]

            total_size = int(content_range[1])

            if length:
                chunk_size = length
            elif offset > index:
                chunk_size = (offset - index) + 1
            elif total_size:
                chunk_size = total_size
            else:
                raise HTTPException(416)
        elif length:
            chunk_size = length
            total_size = length
        else:
            raise HTTPException(400)

        stream = environ['wsgi.input']

        body = []

        try:
            temp_file = os.path.join(
                os.path.dirname('/tmp/test_upload/'),
                temp_name)
            with io.open(temp_file, 'a+b') as f:
                f.truncate(index)

                while chunk_size > 0:
                    # buffer size
                    part = stream.read(min(chunk_size, 1024 * 64))
                    if not part:
                        break
                    f.write(part)
                    chunk_size -= len(part)

                file_size = f.tell()

            if file_size == total_size:
                self.status = 200
            else:
                self.status = 201
                body.append('%d-%d/%d' % (index, offset, total_size))

            self.log.info(dict((x, y) for x, y in (
                ('index', index),
                ('offset', offset),
                ('size', total_size),
                ('temp_file', temp_file),
                ('status', self.status),
                #('env', environ),
            )))

            start_response(
                getattr(http_status_codes, 'HTTP_%d' %
                        self.status), list(self.headers.items()))
            return body
        except IOError:
            raise HTTPException(
                500,
                title="upload directory [ %s ]doesn't exist" % temp_file,
                display=True)
