# -*- coding: utf-8 -*-

"""
exceptions and decorators
"""

import collections
import json
import logging
import time
from functools import wraps


class HTTPError(Exception):

    def __init__(self, status, title=None, description=None,
                 headers=None, code=None, display=False):
        self.status = status
        self.title = title
        self.description = description
        self.headers = headers
        self.code = code
        self.display = display

    def to_json(self):
        return json.dumps({k: str(v) for k, v in self.__dict__.items()
                           if v and k != 'display'},
                          sort_keys=True,
                          indent=4)


class MethodException(HTTPError):

    def __init__(self, status=405, **kwargs):
        return super(MethodException, self).__init__(status, **kwargs)


class HTTPException(HTTPError):

    def __init__(self, status, **kwargs):
        return super(HTTPException, self).__init__(status, **kwargs)


def allow_methods(*methods):
    """Allow methods decorator
    :param methods:
        list of http methods
    """

    def true_decorator(f):

        @wraps(f)
        def wrapped(self, *args, **kwargs):
            if self.api.method.lower() not in [x.lower()
                                               for x in list(methods)]:
                raise MethodException()
            else:
                return f(self, *args, **kwargs)

        return wrapped

    return true_decorator


class LogFormatter(logging.Formatter):
    converter = time.gmtime

    reserved_keys = [
        'args',
        'asctime',
        'created',
        'exc_info',
        'exc_text',
        'filename',
        'funcName',
        'levelname',
        'levelno',
        'lineno',
        'message',
        'module',
        'msecs',
        'msg',
        'name',
        'pathname',
        'process',
        'processName',
        'relativeCreated',
        'thread',
        'threadName'
    ]

    def __init__(self, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.required_fields = [x.strip("%()") for x in self._fmt.split()]

    def format(self, record):
        indent = record.__dict__.get('indent', None)
        if indent:
            del record.indent

        if isinstance(record.msg, dict):
            def clean_dict(self, d):
                new = {}
                for k, v in d.iteritems():
                    if isinstance(v, dict):
                        v = clean_dict(self, v)
                        new[k] = v
                    else:
                        new[k] = str(v)
                return new
            record.message = clean_dict(self, record.msg)
        else:
            record.message = record.getMessage()

        if "asctime" in self.required_fields:
            ct = self.converter(record.created)
            t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
            record.asctime = "%s,%03d" % (t, record.msecs)

        log_record = {}

        for field in self.required_fields:
            log_record[field] = record.__dict__.get(field)

        for key, value in record.__dict__.iteritems():
            """See https://github.com/madzak/python-json-logger
            this allows to have numeric keys
            """
            if (key not in self.reserved_keys and not (
                    hasattr(key, "startswith") and key.startswith('_')
            )):
                log_record[key] = value

        return json.dumps(log_record, sort_keys=True, indent=indent)


class CaseInsensitiveDict(collections.MutableMapping):
    """from:
    https://github.com/kennethreitz/requests/blob/master/requests/structures.py

    A case-insensitive ``dict``-like object.

    Implements all methods and operations of
    ``collections.MutableMapping`` as well as dict's ``copy``. Also
    provides ``lower_items``.

    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case insensitive:

        cid = CaseInsensitiveDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.

    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.

    """

    def __init__(self, data=None, **kwargs):
        self._store = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def lower_items(self):
        """Like iteritems(), but with all lowercase keys."""
        return (
            (lowerkey, keyval[1])
            for (lowerkey, keyval)
            in self._store.items()
        )

    def __eq__(self, other):
        if isinstance(other, collections.Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    # Copy is required
    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, dict(self.items()))
