# uwsgi --http :8080 --wsgi-file app.py --callable app --master

import os
import zunzuncito

root = 'my_api'

versions = ['v0', 'v1', 'v2']

routes = [
    # ('/.*', 'default'),
    ('/teste', 'test_get', 'GET'),
    ('/teste', 'test_post', 'POST'),
    ('/teste', 'test_put', 'PUT')
]

app = zunzuncito.ZunZun(root, versions, routes, debug=False)
