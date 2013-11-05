"""
default resource
"""
import gevent
import gevent.socket
import json
import logging
from zunzuncito import http_status_codes
from zunzuncito.tools import MethodException, HTTPException, allow_methods

def bg_task():
    for i in range(1, 10):
        print "background task", i
        gevent.sleep(2)


def long_task():
    for i in range(1, 10):
        print i
        gevent.sleep()


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = api.headers.copy()
        self.log = logging.getLogger()
        # self.log.setLevel('DEBUG')
        self.log.setLevel('INFO')
        self.log = logging.LoggerAdapter(
            logging.getLogger(), {
                'rid': api.request_id,
                'indent': 4
            })
        self.log.info(dict((x, y) for x, y in (
            ('API', api.version),
            ('URI', api.URI),
            ('method', api.method)
        )))


    def dispatch(self, environ, start_response):
        t = gevent.spawn(long_task)
        t.join()
        yield "sleeping for 3 seconds...<br/>"
        gevent.sleep(3)
        yield "done<br>"
        yield "getting some ips...<br/>"

        urls = ['www.google.com', 'www.example.com', 'www.python.org', 'projects.unbit.it']
        jobs = [gevent.spawn(gevent.socket.gethostbyname, url) for url in urls]
        gevent.joinall(jobs, timeout=2)

        for j in jobs:
            yield "ip = %s<br/>" % j.value

        gevent.spawn(bg_task)
