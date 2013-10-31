# uwsgi --http :8080 --wsgi-file app.py --callable app --master

import os
import zunzuncito

document_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sandbox/api/')

routes = [
        #('/.*', 'default'),
        ('/teste', 'test_get', 'GET'),
        ('/teste', 'test_post', 'POST'),
        ('/teste', 'test_put', 'PUT')
        ]

app = zunzuncito.ZunZun(document_root, routes)
