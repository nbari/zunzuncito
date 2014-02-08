import zunzuncito
from threading import Thread
from uuid import uuid4
import zunzuncito

root = 'my_api'
app = zunzuncito.ZunZun(root, rid='rid', debug=True)


def start_response(status, headers):
    print status, headers


def fake_req(num):
    environ = {
        'rid': str(uuid4()),
        'REQUEST_URI': '/env',
        'REQUEST_METHOD': 'get',
        'thread': num
    }
    print app(environ, start_response)

threads = []
for i in range(2):
    threads.append(Thread(target=fake_req, args=(i,)))
for t in threads:
    t.start()
for t in threads:
    t.join()
