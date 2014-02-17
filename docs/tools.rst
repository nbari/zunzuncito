tools
=====

`tools <https://github.com/nbari/zunzuncito/blob/master/zunzuncito/tools.py>`_ is a module that containg
a set of classes and functions that help to proccess the reply of the request more easy.

.. code-block:: python
   :linenos:
   :emphasize-lines: 2


   from zunzuncito import tools

   class APIResource(object):

       def dispatch(self, request, response):
           """ your code goes here """

.. toctree::
   :maxdepth: 2

   tools/HTTPException
   tools/MethodException
   tools/allow_methods
   tools/log_json
   tools/clean_dict
   tools/CaseInsensitiveDict
