APIResource class
=================

``APIResource`` is the name of the class that the `ZunZun instance <http://docs.zunzun.io/en/latest/zunzun.html>`_
will call to handle the incoming requests.


.. sidebar:: APIResource.dispatch

   The `ZunZun <en/latest/zunzun.html>`_ instance always will call the ``dispath`` method
   that belongs  to the APIResource class.


.. code-block:: python
   :linenos:
   :emphasize-lines: 4

   from zunzuncito import tools


   class APIResource(object):

      def dispatch(self, request, response):

          request.log.debug(tools.log_json({
              'API': request.version,
              'URI': request.URI,
              'method': request.method,
              'vroot': request.vroot
          }, True))

          # print all the environ
          return tools.log_json(request.environ, 4)


For example, the following request::

    http://127.0.0.1:8080/v0/upload

Is handled by the custom python module ``zun_upload/zun_upload.py`` which contents:


.. code-block:: python
   :linenos:
   :emphasize-lines: 12,14,15

   """
   upload resource

   Upload by chunks

   @see http://www.grid.net.ru/nginx/resumable_uploads.en.html
   """
   import os
   from zunzuncito import tools


   class APIResource(object):

       @tools.allow_methods('post, put')
       def dispatch(self, request, response):
           try:
               temp_name = request.path[0]
           except:
               raise tools.HTTPException(400)

           """rfc2616-sec14.html
           see http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
           see http://www.grid.net.ru/nginx/resumable_uploads.en.html
           """
           content_range = request.environ.get('HTTP_CONTENT_RANGE', 0)

           length = int(request.environ.get('CONTENT_LENGTH', 0))

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

           stream = request.environ['wsgi.input']

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
                   response.status = 200
               else:
                   response.status = 201
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

               return body
           except IOError:
               raise tools.HTTPException(
                   500,
                   title="upload directory [ %s ]doesn't exist" % temp_file,
                   display=True)



.. note::

   All the custom modules must have the **APIResource** class and the method **dispatch** in
   order to work
