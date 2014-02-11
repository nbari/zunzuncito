"""
gevent resource
"""

import gevent
import gevent.socket

from zunzuncito import tools


def bg_task():
    for i in range(1, 10):
        print "background task", i
        gevent.sleep(2)


def long_task():
    for i in range(1, 10):
        print i
        gevent.sleep()


class APIResource(object):

    def __init__(self):
        self.headers = {'Content-Type': 'text/html; charset=UTF-8'}

    def dispatch(self, request, response):

        request.log.debug(tools.log_json({
            'API': request.version,
            'Method': request.method,
            'URI': request.URI,
            'vroot': request.vroot
        }, True))

        response.headers.update(self.headers)

        """
        not called while yielding
        """
        response.headers['naranjas'] = '----'

        t = gevent.spawn(long_task)
        t.join()

        yield "sleeping for 3 seconds...<br/>"

        gevent.sleep(3)

        yield "done<br/>"

        yield "getting some ips...<br/>"

        urls = [
            'www.google.com',
            'www.example.com',
            'www.python.org',
            'projects.unbit.it']

        jobs = [gevent.spawn(gevent.socket.gethostbyname, url) for url in urls]
        gevent.joinall(jobs, timeout=2)

        for j in jobs:
            yield "ip = %s<br/>" % j.value

        gevent.spawn(bg_task)
