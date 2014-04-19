"""
exceptions and decorators
"""

import collections
import json


class HTTPError(Exception):

    def __init__(self, status, title=None, description=None,
                 headers=None, code=None, display=False, log=True):
        self.code = code
        self.description = description
        self.display = display
        self.headers = headers
        self.log = log
        self.status = status
        self.title = title

    def to_json(self):
        return json.dumps({k: str(v) for k, v in self.__dict__.items()
                           if v and k not in ['display', 'log']},
                          sort_keys=True,
                          indent=4)

    def to_dict(self):
        return self.__dict__


class MethodException(HTTPError):

    def __init__(self, status=405, **kwargs):
        return super(MethodException, self).__init__(status, **kwargs)


class HTTPException(HTTPError):

    def __init__(self, status, **kwargs):
        return super(HTTPException, self).__init__(status, **kwargs)


def allow_methods(methods):
    """Allow methods decorator
    :param methods: list of http methods
    """
    def true_decorator(f):

        def wrapped(self, *args, **kwargs):
            """self is because the allow_methods decorator is called
            within APIResource class
            """
            if args[0].method.lower() not in [x.lower().strip()
                                              for x in methods.split(',')
                                              if x.strip()]:
                raise MethodException()
            else:
                return f(self, *args, **kwargs)

        return wrapped
    return true_decorator


def clean_dict(d):
    """ clean dictionary object to str
    :param dict: dictionary
    """
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = clean_dict(v)
            new[k] = v
        else:
            new[k] = str(v)
    return new


def log_json(log, indent=None):
    return json.dumps(clean_dict(log), sort_keys=True, indent=indent)


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
