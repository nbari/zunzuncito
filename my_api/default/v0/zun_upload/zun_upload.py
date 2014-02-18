"""
upload resource

Upload by chunks

@see http://www.grid.net.ru/nginx/resumable_uploads.en.html
"""
import os
from zunzuncito import tools


class APIResource(object):

    @tools.allow_methods('post, put')
    def dispatch(self, request, response):
        try:
            temp_name = request.path[0]
        except:
            raise tools.HTTPException(400)

        """rfc2616-sec14.html
        see http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        see http://www.grid.net.ru/nginx/resumable_uploads.en.html
        """
        content_range = request.environ.get('HTTP_CONTENT_RANGE', 0)

        length = int(request.environ.get('CONTENT_LENGTH', 0))

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
                raise tools.HTTPException(416)
        elif length:
            chunk_size = total_size = length
            index = 0
            offset = 0
        else:
            raise tools.HTTPException(400)

        stream = request.environ['wsgi.input']

        body = []

        try:
            temp_file = os.path.join(
                os.path.dirname('/tmp/test_upload/'),
                temp_name)

            with open(temp_file, 'a+b') as f:
                original_file_size = f.tell()

                f.seek(index)
                f.truncate()

                bytes_to_write = chunk_size

                while chunk_size > 0:
                    # buffer size
                    chunk = stream.read(min(chunk_size, 1 << 13))
                    if not chunk:
                        break
                    f.write(chunk)
                    chunk_size -= len(chunk)

                f.flush()
                bytes_written = f.tell() - index

                if bytes_written != bytes_to_write:
                    f.truncate(original_file_size)
                    f.close()
                    raise tools.HTTPException(416)

            if os.stat(temp_file).st_size == total_size:
                response.status = 200
            else:
                response.status = 201
                body.append('%d-%d/%d' % (index, offset, total_size))

            request.log.info(tools.log_json({
                'index': index,
                'offset': offset,
                'size': total_size,
                'status': response.status,
                'temp_file': temp_file
            }, True))

            return body
        except IOError:
            raise tools.HTTPException(
                500,
                title="upload directory [ %s ]doesn't exist" % temp_file,
                display=True)
