import zunzuncito
from threading import Thread
from uuid import uuid4
import zunzuncito

root = 'my_api'
app = zunzuncito.ZunZun(root, rid='rid', debug=True)

environ = {
    'rid': str(uuid4()),
    'REQUEST_URI': '/env'
}

start_response = lambda s, h: (s, h)


def fake_req(num):
    print app(environ, start_response)

for i in range(1):
    t = Thread(target=fake_req, args=(i,)).start()
