"""
To clean:
find . -iname "*.pyc" -exec rm -f {} \;

To run:
uwsgi --http :8080 --wsgi-file app.py --callable app --master

uwsgi --http :8080 --wsgi-file app.py --callable app --master --processes 2 --threads 2 --stats 127.0.0.1:8181 --harakiri 30

gunicorn -b :8080 -w4 app:app
"""

import zunzuncito

"""Root
Name of the directory containing the API
"""
root = 'my_api'

"""Versions
Supported versions
"""
versions = ['v0', 'v1', 'v2']

"""Route format:
    :URI: a regex matching the URI by default
    :handler: the python module that will handle the request
    :methods: list of allowed methods (comma separated)
        if none all are accepted
"""
routes = [
    # ('/.*', 'default'),
    ('/teste', 'test_get', 'GET'),
    ('/teste', 'test_post', 'POST'),
    ('/teste', 'test_put', 'PUT')
]

app = zunzuncito.ZunZun(root, versions, routes, debug=False)
