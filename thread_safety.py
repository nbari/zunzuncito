import sys
import time
import zunzuncito

# from profilehooks import profile
from threading import Thread
from uuid import uuid4

root = 'my_api'
versions = ['v0', 'v1']
app = zunzuncito.ZunZun(root, versions, rid='rid', debug=False)


def timeit(f):

    def wrapper(*args, **kv):
        ts = time.time()
        result = f(*args, **kv)
        te = time.time()
        print '%r (%r, %r) %2.5f sec' % (f.__name__, args, kv, te - ts)
        return result

    return wrapper


def start_response(status, headers):
    sys.stdout.write('%s - %s\n' % (status, headers))

#@profile
def fake_req(num):
    for n in range(num):
        environ = {
            'rid': str(uuid4()),
            'REQUEST_URI': '/v1/thread',
            'REQUEST_METHOD': 'get',
            'thread': n
        }
        body = app(environ, start_response)
        sys.stdout.write('%s\n' % body)


@timeit
def main(t, requests):
    threads = []
    for i in range(t):
        threads.append(Thread(target=fake_req, args=(requests,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    # threads, requests
    main(4, 2)
