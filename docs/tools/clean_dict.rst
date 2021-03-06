clean_dict
==========

The ``clean_dict`` is a small recursive function that given a `dictionary <http://docs.python.org/2/tutorial/datastructures.html#dictionaries>`_
will try to 'clean it' converting it to a string::

    clean_dict(dictionary)


It is commonly used in conjunction with the `log_json </en/latest/tools/log_json.html>`_ function.

Example
.......

snippet taken from `zun_self.py <https://github.com/nbari/zunzuncito/blob/master/my_api/default/v0/zun_self/zun_self.py>`_:

.. code-block:: python
   :linenos:
   :emphasize-lines: 5


    def dispatch(self, request, response):

        return (
            json.dumps(
                tools.clean_dict(request.__dict__),
                sort_keys=True,
                indent=4)
        )
        # taking advantage of the tools.log_json
        # return tools.log_json(request.__dict__, 4)
