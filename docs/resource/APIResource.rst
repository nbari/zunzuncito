APIResource class
=================

``APIResource`` is the name of the class that the `ZunZun <http://docs.zunzun.io/en/latest/zunzun.html>`_
instance will call to handle the incoming requests.


For example, the following requests::

    http://127.0.0.1:8080/v0/upload

Is handled by the custom python module ``zun_upload/zun_upload.py`` which contents:

.. sidebar:: APIResource.dispatch

   The `ZunZun <en/latest/zunzun.html>`_ instance always will call the ``dispath`` method
   that belongs  to the APIResource class.

.. code-block:: python
   :linenos:
   :emphasize-lines: 14,29,30

   """
   upload resource

   Upload by chunks

   @see http://www.grid.net.ru/nginx/resumable_uploads.en.html
   """
   import logging
   import os
   from zunzuncito import tools
   from zunzuncito import http_status_codes


   class APIResource(object):

       def __init__(self, api):
           self.api = api
           self.status = 200
           self.headers = api.headers.copy()
           self.log = logging.getLogger()
           self.log.info(tools.log_json({
               'vroot': api.vroot,
               'API': api.version,
               'URI': api.URI,
               'method': api.method
           }, True)
           )

       @tools.allow_methods('post, put')
       def dispatch(self, environ, start_response):
           try:
               temp_name = self.api.path[0]
           except:
               raise tools.HTTPException(400)

           """rfc2616-sec14.html
           see http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
           see http://www.grid.net.ru/nginx/resumable_uploads.en.html
           """
           content_range = environ.get('HTTP_CONTENT_RANGE', 0)

           length = int(environ.get('CONTENT_LENGTH', 0))

           if content_range:
               content_range = content_range.split()[1].split('/')

               index, offset = [int(x) for x in content_range[0].split('-')]

               total_size = int(content_range[1])

               if length:
                   chunk_size = length
               elif offset > index:
                   chunk_size = (offset - index) + 1
               elif total_size:
                   chunk_size = total_size
               else:
                   raise tools.HTTPException(416)
           elif length:
               chunk_size = total_size = length
               index = 0
               offset = 0
           else:
               raise tools.HTTPException(400)

           stream = environ['wsgi.input']

           body = []

           try:
               temp_file = os.path.join(
                   os.path.dirname('/tmp/test_upload/'),
                   temp_name)

               with open(temp_file, 'a+b') as f:
                   original_file_size = f.tell()

                   f.seek(index)
                   f.truncate()

                   bytes_to_write = chunk_size

                   while chunk_size > 0:
                       # buffer size
                       chunk = stream.read(min(chunk_size, 1 << 13))
                       if not chunk:
                           break
                       f.write(chunk)
                       chunk_size -= len(chunk)

                   f.flush()
                   bytes_written = f.tell() - index

                   if bytes_written != bytes_to_write:
                       f.truncate(original_file_size)
                       f.close()
                       raise tools.HTTPException(416)

               if os.stat(temp_file).st_size == total_size:
                   self.status = 200
               else:
                   self.status = 201
                   body.append('%d-%d/%d' % (index, offset, total_size))

               self.log.info(tools.log_json({
                   'index': index,
                   'offset': offset,
                   'size': total_size,
                   'temp_file': temp_file,
                   'status': self.status,
                   'env': environ
               }, True)
               )

               start_response(
                   getattr(http_status_codes, 'HTTP_%d' %
                           self.status), list(self.headers.items()))
               return body
           except IOError:
               raise tools.HTTPException(
                   500,
                   title="upload directory [ %s ]doesn't exist" % temp_file,
                   display=True)



.. note::

   All the custom modules must have the APIResource class and the method dispatch in
   order to work
