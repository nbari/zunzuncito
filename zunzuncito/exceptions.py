"""
exceptions
"""

import json
from functools import wraps


class HTTPError(Exception):

    def __init__(self, status, title=None, description=None, headers=None, code=None):
        self.status = status
        self.title = title
        self.description = description
        self.headers = headers
        self.code = code

    def to_json(self):
        return json.dumps({k: v for k, v in self.__dict__.items() if v}, sort_keys=True, indent=4)


class MethodException(HTTPError):

    def __init__(self, status=405, **kwargs):
        return super(MethodException, self).__init__(status, **kwargs)


class HTTPException(HTTPError):

    def __init__(self, status, **kwargs):
        return super(HTTPException, self).__init__(status, **kwargs)


def allow(*methods):

    def true_decorator(f):

        @wraps(f)
        def wrapped(self, *args, **kwargs):
            if self.app.method.lower() not in [x.lower() for x in list(methods)]:
                raise MethodException()
            else:
                return f(self, *args, **kwargs)

        return wrapped

    return true_decorator
