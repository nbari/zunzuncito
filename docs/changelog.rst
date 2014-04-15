Changelog
=========

0.1.17 (2014-04-15)
...................

* Added the ``add_header`` method to the response class, with the intention to
  allow multiple headers with the same name, example 'Set-Cookie'.

0.1.16 (2014-03-09)
...................

* fixed bug on py_mod to allow sub modules based on the URI to work properly,
  see `URI_module </en/latest/resource/URI_module.html>`_
* fixed __init__ to make custom versions match allowed_URI_chars ``^[\w-]+$``
* changed UUID4 to UUID1

0.1.15 (2014-02-27)
...................

* log when trying to load the _catchall, if no _catchall raise Exception about
  the missing module
* replaced iteritems with items() to be Python 3 compatible

0.1.14 (2014-02-26)
...................

* replaced itertools.ifilter with filter
* improve py_mod if a URI ends with an slash for example:
  http://api.zunzun.io/v1/add/user/, the py_mod will be:
  ``zun_add/zun_user/zun_user.py``

0.1.13 (2014-02-17)
...................

* Added the log option to the HTTPException, if set to True it will log the
  exception otherwise not.

0.1.12 (2014-02-13)
...................

* Fixed core to be `thread safe <http://en.wikipedia.org/wiki/Thread_safety>`_.
* New classes request, response, the dispatch method require this ``dispatch(self, request, response)``.
* lazy load of resources.
* __catchall module


0.1.11 (2014-02-04)
...................

* Fixed bug in `http_status_codes.py <https://github.com/nbari/zunzuncito/blob/master/zunzuncito/http_status_codes.py>`_ when handling generic reasons.

0.1.10 (2014-01-28)
...................

* `dispatch method </en/latest/resource/dispatch_method.html>`_ requires now only one argument, which is **environ**, the start_response is handled by the API it self.
* http_status_codes now is a dictionary.

0.1.9 (2014-01-06)
..................

* self._headers is created only once at the beginning and per request just
  copied to self.headers.

0.1.8 (2014-01-04)
..................

* Fixed tools.log_json function to not indent when no indent value is set.
