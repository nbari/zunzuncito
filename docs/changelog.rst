Changelog
=========

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
