import os
import urllib2
import uuid
from poster.streaminghttp import register_openers
from random import randint
from uuid import uuid4


def read_in_chunks(file_object, chunk_size=65536):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def main(file, url):
    content_name = str(file)
    content_path = os.path.abspath(file)
    content_size = os.stat(content_path).st_size

    print content_name, content_path, content_size

    f = open(content_path)

    index = 0
    offset = 0
    headers = {}
    session_id = str(uuid4())

    register_openers()
    data = read_in_chunks(f)
    request = urllib2.Request(url, data=data)
    request.add_header('Content-Type', 'application/octet-stream')
    request.add_header('Content-Length', content_size)
    request.get_method = lambda: 'PUT'
    rs = urllib2.urlopen(request).read()
    print repr(rs)


if __name__ == '__main__':
    url = 'http://localhost:8080/test_upload/file_name'
    #url = 'http://requestb.in/1kay3pk1'
    #main('images/test_image_%d.jpg' % randint(1, 3), url)
    main('images/test_image_%d.jpg' % 2, url)
