routes = {}
routes['*'] = [
    ('/.*', 'default'),
    ('/teste', 'test_get', 'GET'),
    ('/teste', 'test_post', 'POST'),
    ('/teste', 'test_put', 'PUT'),
    ('/my', 'ip_tools', 'GET'),
    ('/status/?.*', 'http_status', 'GET'),
    ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST')
]
routes['site.com'] = [
    ('/.*', 'default'),
    ('/teste', 'test_get', 'GET'),
    ('/teste', 'test_post', 'POST')
]
routes['www.site.com'] = []
routes['ww.site.com'] = []


HTTP_HOST = 'wwww.site.com:8080'

host = HTTP_HOST.strip().split(':')[0]
sites =  [k for k in sorted(routes, key=len, reverse=True)]

if any(host in s for s in sites):
    print host
else:
    for k in sites:
        if k.endswith(host):
            print host
