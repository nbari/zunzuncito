# -*- coding: utf-8 -*-
"""
nc -l 8080
"""
import requests

requests.post('http://localhost:8080', data={u'post': 'niño coraçao'})

# import urllib
# s = urllib.unquote_plus(b"ni%C3%B1o+cora%C3%A7ao").decode('utf-8')
# print s
