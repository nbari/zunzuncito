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

"""hosts dictionary
Multitenant support
    :host: a host to match
    :vroot: the document root for this host root/vroot
        the vroot name should exists in the routes dictionary
    data structure to follow:
        {
            'host': 'vroot',
            'host1': 'vroot1
        }
"""
hosts = {
    '*': 'default',
    'api.zunzun.io': 'default',
    'beta.zunzun.io': 'beta_zunzun_io'
}

"""Routes dictionary
    :vroot: the document root for this host root/vroot
        the vroot name should exists in the hosts dictionary
    :pattern: a regex to match the URI path
    :resource: the python module that will handle the request
    :methods: list of allowed methods, defaults to ALL (optional)
    data structure to follow:
        {
            'vroot': [(regex,resource,methods)],
            'vroot1': [(regex,resource,methods)]
        }
"""
routes = {}
routes['default'] = [
    ('/teste', 'test_get', 'GET'),
    ('/teste', 'test_post', 'POST'),
    ('/teste', 'test_put', 'PUT'),
    ('/my/?.*', 'ip_tools', 'GET'),
    ('/status/?.*', 'http_status', 'GET'),
    ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
    ('/.*', 'default')
]
routes['beta_zunzun_io'] = [
    ('/.*', 'default'),
]

app = zunzuncito.ZunZun(
    root,
    versions,
    hosts,
    routes,
    rid='TRACK_ID',
    debug=False)
