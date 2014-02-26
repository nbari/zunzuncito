Changelog
=========

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
