import zunzuncito
from threading import Thread
from uuid import uuid4
import zunzuncito

root = 'my_api'
app = zunzuncito.ZunZun(root, rid='rid')

environ = {
    'rid': str(uuid4()),
    'REQUEST_URI': '/self'
}
start_response = lambda s, h: (s, h)

for i in range(3):
    t = Thread(target=app, args=(environ, start_response,)).start()
