import unittest
import zunzuncito


class ZunZunTest(unittest.TestCase):
    versions = ['  ', '', 1, 'v0', 'my version', (1,)]

    routes = [
        ('/.*', 'default'),
        ('/teste', 'test_put', 'PUT'),
        ('^/teste', 'test_put', 'PUT'),
        ('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'),
        ('/?')
    ]

    def test_versions(self):
        zun = zunzuncito.ZunZun('/tmp', self.versions)
        self.assertEqual(4, len(zun.versions))

    def test_register_routes(self):
        zun = zunzuncito.ZunZun('/tmp', self.versions, self.routes)
        zun_routes = zun.routes

        for regex, pattern in zip(self.routes, zun_routes):
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


if __name__ == '__main__':
    unittest.main()
