"""
python text.py
"""

import sys
import unittest
import zunzuncito

from threading import Thread
from uuid import uuid4
from zunzuncito import tools


def py_version(f):
    def wrapper(*args, **kv):
        if sys.version_info < (3, 3):
            return f(*args, **kv)
        return True
    return wrapper


class ZunZunTest(unittest.TestCase):
    versions = ['  ', '', 1, 'v0', 'my version', (1,), 'api/v1', 'v1', 'v2 ']

    hosts = {
        '*': 'default',
        'api.zunzun.io': 'default',
        'beta.zunzun.io': 'beta_zunzun_io',
        'oauth.zunzun.io': 'oauth',
        'oic.zunzun.io': 'oic'
    }

    routes = {
        'default':
        [
            ('/.*', 'default'),
            ('/teste', 'test_put', 'PUT'),
            ('^/teste', 'test_put', 'PUT'),
            ('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
             'uuid'),
            ('/?', 'xxx'),
            ('/.*', 'default')
        ],
        'other':
        [
            (r'/(.*\.(gif|png|jpg|ico|bmp|css|otf|woff))', 'static')
        ]
    }

    def test_versions(self):
        app = zunzuncito.ZunZun('/tmp', self.versions)
        self.assertEqual(3, len(app.versions))

    def test_hosts(self):
        app = zunzuncito.ZunZun('/tmp', self.versions, self.hosts)
        self.assertEqual(len(self.hosts), len(app.hosts))

    def test_register_routes(self):
        app = zunzuncito.ZunZun('/tmp', routes=self.routes)

        for k in self.routes.keys():
            self.assertEqual(len(self.routes[k]), len(app.routes[k]))
            for regex, pattern in zip(self.routes[k], app.routes[k]):
                # print regex[0], pattern[0].pattern
                if regex[0].startswith('^'):
                    if regex[0] != pattern[0].pattern:
                        self.assertTrue(False)
                        break
                else:
                    if '^%s$' % regex[0] != pattern[0].pattern:
                        self.assertTrue(False)
                        break

        self.assertTrue(True)

    def test_rid_unique(self):
        app = zunzuncito.ZunZun('my_api', rid='rid')
        out = []

        def start_response(status, headers):
            self.assertFalse(headers[0][1] in out)
            out.append(headers[0][1])

        for environ in fake_req(1000):
            body = app(environ, start_response)

        self.assertEqual(1000, len(out))

    @py_version
    def test_Thread_safety(self):
        app = zunzuncito.ZunZun('my_api', rid='rid')
        out = []
        body = []

        def start_response(status, headers):
            self.assertFalse(headers[0][1] in out)
            out.append(headers[0][1])

        def make_req(times):
            for environ in fake_req(times):
                body.append(app(environ, start_response))

        """ num of threads t, and num or requests r """
        t = 4
        r = 250
        threads = []
        for _ in range(t):
            threads.append(Thread(target=make_req, args=(r,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        """ out = threads x request t*r"""
        self.assertEqual(1000, len(out))

        """ check if list are equals """
        self.assertTrue(set(out) == set(body))

    def test_status_200(self):
        app = zunzuncito.ZunZun('my_api')

        def start_response(status, headers):
            self.assertTrue(status.startswith('200'))

        environ = list(fake_req(1, '/test'))
        body = app(environ[0], start_response)

    def test_status_xxx(self):
        app = zunzuncito.ZunZun('my_api', self.versions)

        for i in range(100, 600, 100):
            def start_response(status, headers):
                self.assertTrue(status.startswith(str(i)))

            environ = list(fake_req(1, '/v1/test/%s' % i))
            body = app(environ[0], start_response)

        for i in range(100, 600, 99):
            def start_response(status, headers):
                self.assertTrue(status.startswith(str((i // 100) * 100)))

            environ = list(fake_req(1, '/v1/test/%s' % i))
            body = app(environ[0], start_response)


def fake_req(num, uri='/test'):
    i = 0
    while i < num:
        environ = {
            'rid': str(uuid4()),
            'REQUEST_URI': uri,
            'REQUEST_METHOD': 'get'
        }
        yield environ
        i += 1

if __name__ == '__main__':
    unittest.main()
