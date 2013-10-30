"""
exceptions
"""
import json


class APIException(Exception):

    def __init__(self, status, title=None, description=None, headers=None, code=None):
        self.status = status
        self.title = title
        self.description = description
        self.headers = headers
        self.code = code

    def to_json(self):
        return json.dumps({k: v for k, v in self.__dict__.items()}, sort_keys=True, indent=4)


class MethodException(APIException):

    def __init__(self, status=405, **kwargs):
        return super(MethodException, self).__init__(self, status, **kwargs)


class HTTPException(APIException):

    def __init__(self, status, **kwargs):
        return super(MethodException, self).__init__(self, status, **kwargs)
