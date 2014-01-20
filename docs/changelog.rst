Changelog
=========


0.1.9 (2014-01-06)
................

* self._headers is created only once at the beginning and per request just
  copied to self.headers

0.1.8 (2014-01-04)
................

* Fixed tools.log_json function to not indent when no indent value is set.
