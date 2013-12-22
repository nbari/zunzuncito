CaseInsensitiveDict
===================

A case-insensitive ``dict``-like object.
.. note::

    Class taken from: `requests <https://github.com/kennethreitz/requests/blob/master/requests/structures.py>`_


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
