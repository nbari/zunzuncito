import os
import requests
import uuid
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

    for chunk in read_in_chunks(f):
        offset = index + len(chunk)
        headers['Content-Type'] = 'application/octet-stream'
        headers['Content-length'] = content_size
        headers['Content-Range'] = 'bytes %s-%s/%s' % (index, offset, content_size)
        headers['Session-ID'] = session_id
        index = offset
        try:
            r = requests.put(url, data=chunk, headers=headers)
            print "r: %s, Content-Range: %s" % (r, headers['Content-Range'])
        except Exception, e:
            print e


if __name__ == '__main__':
    url = 'http://localhost:8080/test_upload/file_name'
    #url = 'http://requestb.in/1kay3pk1'
    main('images/test_image_%d.jpg' % randint(1,3), url)
