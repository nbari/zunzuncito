import zunzuncito
from threading import Thread
from uuid import uuid4
import zunzuncito

root = 'my_api'
app = zunzuncito.ZunZun(root, rid='rid', debug=True)

environ = {
    'rid': str(uuid4()),
    'REQUEST_URI': '/env',
    'REQUEST_METHOD': 'get'
}


def start_response(status, headers):
    print status, headers


def fake_req(num):
    environ.update({'thread': num})
    print app(environ, start_response)

threads = []
for i in range(1):
    threads.append(Thread(target=fake_req, args=(i,)))
for t in threads:
    t.start()
for t in threads:
    t.join()
